import sys
# sys.path.insert(0, "./expressions")
# sys.path.insert(0, "./misc")

from eggscript_src.config import get_config
import traceback

from eggscript_src.expressions.expression import keyword_regexes

from eggscript_src.expressions.array_access_expression import ArrayAccessExpression
from eggscript_src.expressions.break_expression import BreakExpression
from eggscript_src.expressions.case_expression import CaseExpression
from eggscript_src.expressions.chaining_expression import ChainingExpression
from eggscript_src.misc.comment import Comment
from eggscript_src.expressions.conditional_expression import ConditionalExpression
from eggscript_src.expressions.continue_expression import ContinueExpression
from eggscript_src.expressions.datablock_expression import DatablockExpression
from eggscript_src.expressions.default_expression import DefaultExpression
from eggscript_src.file import File
from eggscript_src.expressions.for_loop_expression import ForLoopExpression
from eggscript_src.expressions.function_expression import FunctionExpression
from eggscript_src.expressions.inheritance_expression import InheritanceExpression
from eggscript_src.misc.literal import Literal
from eggscript_src.expressions.method_expression import MethodExpression
from eggscript_src.expressions.namespace_expression import NamespaceExpression
from eggscript_src.expressions.new_object_expression import NewObjectExpression
from eggscript_src.expressions.operator_expression import OperatorExpression
from eggscript_src.expressions.package_expression import PackageExpression
from eggscript_src.expressions.parentheses_expression import ParenthesesExpression
from eggscript_src.expressions.postfix_expression import PostfixExpression
from eggscript_src.expressions.template_literal_expression import TemplateLiteralExpression
from eggscript_src import regex
from eggscript_src.expressions.return_expression import ReturnExpression
from eggscript_src.misc.string_literal import StringLiteral
from eggscript_src.misc.symbol import Symbol
from eggscript_src.expressions.switch_expression import SwitchExpression
from eggscript_src.expressions.variable_assignment_expression import VariableAssignmentExpression
from eggscript_src.misc.variable_symbol import VariableSymbol
from eggscript_src.expressions.vector_escape_expression import VectorEscapeExpression
from eggscript_src.expressions.vector_expression import VectorExpression
from eggscript_src.expressions.vector_length_expression import VectorLengthExpression
from eggscript_src.expressions.while_loop_expression import WhileLoopExpression

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

	def tokenize(
		self,
		stop_ats = [],
		give_back_stop_ats = [],
		buffer_give_back_stop_at = [],
		inheritable_give_back_stop_at = [],
		tree = None,
		read_spaces = False,
		vector_mode = False
	):
		self.buffer = ""
		while True:
			char = ''
			try:
				char = self.file.read_character(ignore_whitespace=not read_spaces)
			except:
				break

			try:
				# handle keyword matching (function, for, if, etc)
				if(
					vector_mode == False
					and regex.keywords.match(self.buffer)
					and regex.keywords.match(self.buffer + char) == None
					and (
						regex.valid_symbol.match(self.buffer + char) == None
						or self.file.skipped_space
					)
					and tree.no_keywords_in_code_block == False
				):
					for keyword_regex, expression_class in keyword_regexes.items():
						if keyword_regex.match(self.buffer):
							self.add_expression(tree, expression_class.read_expression(self, tree))
							self.buffer = ""
							break
					
					continue
				
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
			
				if (
					(
						regex.operator_token.match(char)
						and (
							self.file.current_line_index > self.operator_ban[0]
							or self.file.current_index > self.operator_ban[1]
						)
					) or (
						vector_mode
						and regex.vector_cross_token.match(char)
					)
				): # handle operators
					if regex.comma_token.match(char): # handle commas in special case
						if tree.has_arguments:
							self.absorb_buffer(tree)
							tree.convert_expressions_to_arguments()
						continue
					elif vector_mode == False:
						operator = OperatorExpression.read_expression(self)
						if operator != None:
							self.absorb_buffer(tree)
							if regex.valid_comment.match(operator.operator):
								comment = Comment.read_expression(self)
								if get_config("nocomments") != True:
									self.add_expression(tree, comment)
							elif regex.valid_assignment.match(operator.operator):
								# take last expression and use that as left hand for variable assignment
								last_expression = tree.expressions.pop()
								new_expression = VariableAssignmentExpression.read_expression(self, operator, last_expression, stop_ats)
								last_expression.parent = new_expression
								self.add_expression(tree, new_expression)
							elif regex.valid_postfix.match(operator.operator):
								# take last expression and use that for postfix operation
								last_expression = tree.expressions.pop()
								new_expression = PostfixExpression(last_expression, operator, tokenizer=self)
								last_expression.parent = new_expression
								self.add_expression(tree, new_expression)
							elif regex.valid_template_string.match(operator.operator):
								self.add_expression(tree, StringLiteral.read_expression(self, is_template=True))
							else:
								self.add_expression(tree, operator)
						continue
					elif vector_mode == True: # when in vector mode, don't attempt to read a multi-character operator and instead dump what we find straight to expression
						if regex.valid_vector_operators.match(char):
							self.absorb_buffer(tree)
							self.add_expression(tree, OperatorExpression(char, tokenizer=self))
							continue
					
				if (
					regex.chaining_token.match(char)
					and regex.valid_symbol.match(self.buffer)
					and regex.valid_symbol.match(self.file.peek_next_character())
					or (
						len(tree.expressions) > 0
						and tree.expressions[-1].is_chainable
						and regex.valid_symbol.match(self.buffer) == None
					)
				): # handle chaining (%test.test.test.test...)
					self.add_expression(tree, ChainingExpression.read_expression(self, tree, inheritable_give_back_stop_at))
					self.buffer = "" # absorb buffer
				elif regex.namespace_token.match(char): # handle namespaces ($Test::frog:egg...)
					if regex.valid_symbol.match(self.buffer):
						# if we have a valid symbol, then build chaining expression from remaining valid symbols
						self.add_expression(tree, NamespaceExpression.read_expression(self, inheritable_give_back_stop_at))
						self.buffer = "" # absorb buffer
					else:
						raise Exception(f"Invalid symbol for namespace expression '{self.buffer}'")
				elif regex.semicolon_token.match(char):
					# just absorb the character and move on, we have automatic semicolon placement
					self.absorb_buffer(tree)
				elif regex.string_token.match(char): # handle strings (except for template strings)
					self.add_expression(tree, StringLiteral.read_expression(self))
				elif regex.vector_token.match(char): # handle vector operations
					self.add_expression(tree, VectorExpression.read_expression(self))
				elif regex.parentheses_token.match(char):
					if regex.opening_parenthesis_token.match(char) and regex.valid_symbol.match(self.buffer) == None: # handle math parentheses
						self.add_expression(tree, ParenthesesExpression.read_expression(self, vector_mode=vector_mode))
					elif regex.opening_parenthesis_token.match(char) and regex.valid_symbol.match(self.buffer) != None: # handle method parentheses
						self.add_expression(tree, MethodExpression.read_expression(self, vector_mode=vector_mode))
				elif regex.opening_bracket_token.match(char): # handle array accessing
					self.add_expression(tree, ArrayAccessExpression.read_expression(self))
					self.buffer = ""
				elif (
					vector_mode
					and regex.vector_dot_token.match(char)
				): # handle vector dots in special case
					self.add_expression(tree, OperatorExpression(char, tokenizer=self))
					self.buffer = ""
				elif (
					vector_mode
					and regex.vector_escape_token.match(char)
				):
					self.add_expression(tree, VectorEscapeExpression.read_expression(self))
					self.buffer = ""
				elif (
					vector_mode
					and regex.vector_length_token.match(char)
				):
					self.add_expression(tree, VectorLengthExpression.read_expression(self))
					self.buffer = ""
				else: # when in doubt, add to buffer
					self.buffer = self.buffer + char
			except Exception as error:
				if get_config("verbose") == True:
					traceback.print_exc()

				print(f"\033[91mEncountered exception '{error.__str__()}' at line #{self.file.current_line_index} character #{self.file.current_index}\033[0m")
				return None

		return tree