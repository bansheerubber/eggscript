import sys
sys.path.insert(0, "./expressions")
sys.path.insert(0, "./misc")

from config import get_config
import traceback

from expression import keyword_regexes

from array_access_expression import ArrayAccessExpression
from break_expression import BreakExpression
from case_expression import CaseExpression
from chaining_expression import ChainingExpression
from comment import Comment
from conditional_expression import ConditionalExpression
from continue_expression import ContinueExpression
from datablock_expression import DatablockExpression
from default_expression import DefaultExpression
from file import File
from for_loop_expression import ForLoopExpression
from function_expression import FunctionExpression
from inheritance_expression import InheritanceExpression
from literal import Literal
from method_expression import MethodExpression
from namespace_expression import NamespaceExpression
from new_object_expression import NewObjectExpression
from operator_expression import OperatorExpression
from package_expression import PackageExpression
from parentheses_expression import ParenthesesExpression
from postfix_expression import PostfixExpression
from template_literal_expression import TemplateLiteralExpression
from tokenizer_exception import TokenizerException
import regex
from return_expression import ReturnExpression
from string_literal import StringLiteral
from symbol import Symbol
from switch_expression import SwitchExpression
from variable_assignment_expression import VariableAssignmentExpression
from variable_symbol import VariableSymbol
from while_loop_expression import WhileLoopExpression

class Tokenizer:
	def __init__(self, file):
		self.file = file
		self.operator_ban = (-1, -1)
	
	def absorb_buffer(self, tree):
		if self.buffer.strip() == "":
			self.buffer = ""
		elif regex.digits.match(self.buffer):
			self.add_expression(tree, Literal(self.buffer))
			self.buffer = ""
		elif regex.valid_symbol.match(self.buffer):
			self.add_expression(tree, self.get_symbol(self.buffer))
			self.buffer = ""
	
	def read_comment(self):
		while self.file.give_character_back() != "/":
			pass
		self.file.give_character_back()
			
		# read the rest of the line
		comment = self.file.absorb_line()
		return Comment(comment)

	def read_variable_assignment(self, operator, left_hand, stop_ats):
		# keep reading until we absorb the full value (ended by semicolon)
		expression = VariableAssignmentExpression(operator, left_hand)
		self.tokenize(stop_ats=[regex.semicolon_token] + stop_ats, give_back_stop_ats=[regex.semicolon_token] + stop_ats, tree=expression)
		return expression
	
	def read_parentheses_expression(self):
		expression = ParenthesesExpression()
		self.tokenize(stop_ats=[regex.closing_parenthesis_token], tree=expression)
		return expression
	
	def read_method_expression(self, method_name):
		expression = MethodExpression(method_name)
		self.tokenize(stop_ats=[regex.closing_parenthesis_token], give_back_stop_ats=[regex.semicolon_token], tree=expression)
		expression.convert_expressions_to_arguments()
		return expression
	
	def read_array_access_expression(self):
		expression = ArrayAccessExpression(self.get_symbol(self.buffer))
		self.buffer = ""
		self.tokenize(stop_ats=[regex.closing_bracket_token], give_back_stop_ats=[regex.semicolon_token], tree=expression)
		expression.convert_expressions_to_arguments()
		return expression

	def read_string(self):
		self.file.give_character_back()
		delimiter = self.file.read_character()
		
		has_ended = False
		output = [''] # list of values with templates inbetween them
		template_literal = None
		while has_ended == False:
			char = self.file.read_character(ignore_whitespace=False)
			# if we read a backslash, imeditally read the next character so we don't trip up on \" or \'
			if char == "\\":
				output[len(output) - 1] = output[len(output) - 1] + char + self.file.read_character(ignore_whitespace=False)
				continue
			elif regex.template_literal_token.match(char):
				if template_literal == None:
					template_literal = TemplateLiteralExpression() # create template literal if we don't have one
				# tokenize b/c we're parsing runnable code
				self.tokenize(stop_ats=[regex.template_literal_token], tree=template_literal)
				# move the templates over to a new list
				template_literal.add_template()
				# add a new value
				output.append('')
			elif char == delimiter: # find the last " or '
				has_ended = True
			else: # add to the value
				output[len(output) - 1] = output[len(output) - 1] + char

		if template_literal == None:
			return StringLiteral(output[0], delimiter)
		else:
			template_literal.strings = output
			return template_literal
	
	def read_chaining_expression(self, tree, inheritable_give_back_stop_at):
		first_expression = None
		if len(tree.expressions) > 0 and tree.expressions[-1].is_chainable:
			first_expression = tree.expressions.pop()
		else:
			first_expression = self.get_symbol(self.buffer)
			self.buffer = ""
		
		chaining_expression = ChainingExpression()
		self.add_expression(chaining_expression, first_expression)
		try:
			self.file.give_character_back()
			while self.file.read_character() == ".":
				self.tokenize(stop_ats=[], give_back_stop_ats=inheritable_give_back_stop_at + [regex.semicolon_token, regex.chaining_token, regex.operator_token_without_concatenation, regex.closing_parenthesis_token, regex.closing_bracket_token], tree=chaining_expression)
			self.file.give_character_back()
		except:
			pass # if we hit an EOF, just ignore it

		return chaining_expression
	
	def read_namespace_expression(self, first_symbol_name, inheritable_give_back_stop_at):
		namespace_expression = NamespaceExpression()
		self.add_expression(namespace_expression, self.get_symbol(first_symbol_name))
		try:
			self.file.give_character_back()
			while self.file.read_character() == ":" and self.file.read_character() == ":":
				self.tokenize(stop_ats=[], give_back_stop_ats=inheritable_give_back_stop_at + [regex.semicolon_token, regex.namespace_token, regex.operator_token_without_concatenation, regex.closing_parenthesis_token, regex.closing_bracket_token, regex.chaining_token], tree=namespace_expression)
			self.file.give_character_back()
		except:
			pass # if we hit an EOF, just ignore it
			
		return namespace_expression
	
	def read_operator(self):
		self.file.give_character_back()
		buffer = ""
		operator_ban_space = 0
		saved_operator = None
		index = 0
		while True:
			char = self.file.read_character(ignore_whitespace=False)
			if regex.operator_token.match(char) or regex.part_of_operator.match(char):
				buffer = buffer + char
			else:
				operator_ban_space = index
				break
			
			if regex.valid_operator.match(buffer):
				saved_operator = buffer
			
			index = index + 1

		if saved_operator != None:
			difference = len(buffer) - len(saved_operator)
			for i in range(0, difference + 1):
				self.file.give_character_back()
			
			# special case for namespaces and modulus
			next_char = self.file.read_character()
			if (
				(next_char == ":" and saved_operator == ":")
				or (regex.modulus_next_character_token.match(next_char) == None and saved_operator == "%")
			):
				self.file.give_character_back()
				self.file.give_character_back()
				self.operator_ban = (self.file.current_line_index, self.file.current_index + operator_ban_space)
				return None
			else:
				self.file.give_character_back()
			
			return OperatorExpression(saved_operator)
		else:
			for i in range(0, operator_ban_space + 1):
				self.file.give_character_back()
			self.operator_ban = (self.file.current_line_index, self.file.current_index + operator_ban_space)
			return None
	
	def get_symbol(self, symbol_name):
		if regex.variable_token.match(symbol_name[0]):
			return VariableSymbol(symbol_name)
		else:
			return Symbol(symbol_name)
	
	def add_expression(self, tree, expression):
		tree.expressions.append(expression)
		expression.parent = tree
	
	def update_last_expression(self, tree, new_expression):
		self.add_expression(new_expression, tree.expressions.pop())

	def tokenize(self, stop_ats=[], give_back_stop_ats=[], buffer_give_back_stop_at=[], inheritable_give_back_stop_at=[], tree=None, read_spaces=False):
		self.buffer = ""
		while True:
			char = ''
			try:
				char = self.file.read_character(ignore_whitespace=not read_spaces)
			except:
				break
			
			try:
				for stop_at in buffer_give_back_stop_at:
					if stop_at.match(self.buffer):
						self.file.current_index = self.file.current_index - len(self.buffer) - 2
						self.buffer = ""
						return tree
			
				for stop_at in give_back_stop_ats:
					if stop_at.match(char):
						self.absorb_buffer(tree)
						self.file.give_character_back()
						return tree
				
				for stop_at in stop_ats:
					if stop_at.match(char):
						self.absorb_buffer(tree)
						return tree
				
				# handle keyword matching (function, for, if, etc)
				if(
					regex.keywords.match(self.buffer)
					and regex.keywords.match(self.buffer + char) == None
					and (
						regex.valid_symbol.match(self.buffer + char) == None
						or self.file.skipped_space
					)
					and tree.no_keywords_in_code_block == False
				):
					for keyword_regex, expression_class in keyword_regexes.items():
						if keyword_regex.match(self.buffer):
							self.add_expression(tree, expression_class.read_expression(self))
							self.buffer = ""
							break
					
					continue
			
				if (
					regex.operator_token.match(char)
					and (
						self.file.current_line_index > self.operator_ban[0]
						or self.file.current_index > self.operator_ban[1]
					)
				): # handle operators
					if regex.comma_token.match(char): # handle commas in special case
						if tree.has_arguments:
							self.absorb_buffer(tree)
							tree.convert_expressions_to_arguments()
					else:
						operator = self.read_operator()
						if operator != None:
							self.absorb_buffer(tree)
							if regex.valid_comment.match(operator.operator):
								comment = self.read_comment()
								if get_config("nocomments") != True:
									self.add_expression(tree, comment)
							elif regex.valid_assignment.match(operator.operator):
								# take last expression and use that as left hand for variable assignment
								last_expression = tree.expressions.pop()
								new_expression = self.read_variable_assignment(operator, last_expression, stop_ats)
								last_expression.parent = new_expression
								self.add_expression(tree, new_expression)
							elif regex.valid_postfix.match(operator.operator):
								# take last expression and use that for postfix operation
								last_expression = tree.expressions.pop()
								new_expression = PostfixExpression(last_expression, operator)
								last_expression.parent = new_expression
								self.add_expression(tree, new_expression)
							else:
								self.add_expression(tree, operator)
				elif (regex.chaining_token.match(char)
					and regex.valid_symbol.match(self.buffer)
					or (
						len(tree.expressions) > 0
						and tree.expressions[-1].is_chainable
						and regex.valid_symbol.match(self.buffer) == None
					)
				): # handle chaining (%test.test.test.test...)
					self.add_expression(tree, self.read_chaining_expression(tree, inheritable_give_back_stop_at))
					self.buffer = "" # absorb buffer
				elif regex.namespace_token.match(char): # handle namespaces ($Test::frog:egg...)
					if regex.valid_symbol.match(self.buffer):
						# if we have a valid symbol, then build chaining expression from remaining valid symbols
						self.add_expression(tree, self.read_namespace_expression(self.buffer, inheritable_give_back_stop_at))
						self.buffer = "" # absorb buffer
					else:
						raise Exception(f"Invalid symbol for namespace expression '{self.buffer}'")
				elif regex.semicolon_token.match(char):
					# just absorb the character and move on, we have automatic semicolon placement
					self.absorb_buffer(tree)
				elif regex.string_token.match(char): # handle strings
					string = self.read_string()
					self.add_expression(tree, string)
				elif regex.parentheses_token.match(char):
					if regex.opening_parenthesis_token.match(char) and regex.valid_symbol.match(self.buffer) == None: # handle math parentheses
						self.add_expression(tree, self.read_parentheses_expression())
					elif regex.opening_parenthesis_token.match(char) and regex.valid_symbol.match(self.buffer) != None: # handle method parentheses
						self.add_expression(tree, self.read_method_expression(self.buffer))
				elif regex.opening_bracket_token.match(char): # handle array accessing
					self.add_expression(tree, self.read_array_access_expression())
					self.buffer = ""
				else: # when in doubt, add to buffer
					self.buffer = self.buffer + char
			except Exception as error:
				traceback.print_stack()
				print(f"Encountered exception '{error.__str__()}' at line #{self.file.line_count} character #{self.file.current_index}")
				return None

		return tree