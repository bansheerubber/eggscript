from case_expression import CaseExpression
from chaining_expression import ChainingExpression
from comment import Comment
from conditional_expression import ConditionalExpression
from default_expression import DefaultExpression
from file import File
from for_loop_expression import ForLoopExpression
from function_expression import FunctionExpression
from literal import Literal
from method_expression import MethodExpression
from namespace_expression import NamespaceExpression
from operator_expression import OperatorExpression
from package_expression import PackageExpression
from parentheses_expression import ParenthesesExpression
from postfix_expression import PostfixExpression
from template_literal import TemplateLiteral
from tokenizer_exception import TokenizerException
from regex import chaining_token, closing_bracket_token, closing_parenthesis_token, colon_token, comma_token, digits, keywords, namespace_token, opening_bracket_token, opening_parenthesis_token, operator_token, operator_token_only_concatenation, operator_token_without_concatenation, parentheses_token, template_literal_token, semicolon_token, string_token, valid_assignment, valid_case, valid_conditional, valid_comment, valid_default, valid_for, valid_function, valid_operator, valid_package, valid_postfix, valid_symbol, valid_switch, valid_switch_string, valid_while, variable_token
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
		elif digits.match(self.buffer):
			self.add_expression(tree, Literal(self.buffer))
			self.buffer = ""
		elif valid_symbol.match(self.buffer):
			self.add_expression(tree, self.get_symbol(self.buffer))
			self.buffer = ""
	
	def read_comment(self):
		self.file.give_character_back()
		self.file.give_character_back()
		# read the rest of the line
		comment = self.file.absorb_line()
		return Comment(comment)
	
	def read_for_loop(self):
		expression = ForLoopExpression()
		
		self.tokenize(stop_ats=[semicolon_token], tree=expression)
		expression.move_initiation_expressions()

		self.tokenize(stop_ats=[semicolon_token], tree=expression)
		expression.move_conditional_expressions()

		self.tokenize(stop_ats=[closing_parenthesis_token], tree=expression)
		expression.move_increment_expressions()

		self.file.read_character() # absorb first "{"
		self.tokenize(stop_ats=[closing_bracket_token], tree=expression)

		return expression
	
	def read_while_loop(self):
		expression = WhileLoopExpression()
		
		self.tokenize(stop_ats=[closing_parenthesis_token], tree=expression)
		expression.convert_expressions_to_conditionals()

		self.file.read_character() # absorb first "{"
		self.tokenize(stop_ats=[closing_bracket_token], tree=expression)

		return expression
	
	def read_default(self):
		expression = DefaultExpression()
		# read up until next case, next default, or }
		self.tokenize(give_back_stop_ats=[closing_bracket_token], buffer_give_back_stop_at=[valid_case, valid_default], tree=expression)

		return expression
	
	def read_case(self):
		expression = CaseExpression()
		self.file.give_character_back()
		self.tokenize(stop_ats=[colon_token], tree=expression)
		expression.convert_expressions_to_conditionals()

		# read up until next case, next default, or }
		self.tokenize(give_back_stop_ats=[closing_bracket_token], buffer_give_back_stop_at=[valid_case, valid_default], tree=expression)

		return expression
	
	def read_switch(self):
		self.file.give_character_back()
		self.file.give_character_back()
		char = self.file.read_character()
		switch_type = "switch"
		if char == "$":
			switch_type = "switch$"
		else:
			self.file.read_character()
		
		expression = SwitchExpression(switch_type)
		
		self.tokenize(stop_ats=[closing_parenthesis_token], tree=expression)
		expression.convert_expressions_to_conditionals()

		self.file.read_character() # absorb first "{"
		self.tokenize(stop_ats=[closing_bracket_token], tree=expression)

		return expression
	
	def read_package(self):
		expression = PackageExpression()

		self.file.give_character_back()

		self.tokenize(stop_ats=[opening_bracket_token], tree=expression)
		expression.convert_expression_to_name()

		self.tokenize(stop_ats=[closing_bracket_token], tree=expression)

		return expression
	
	def read_function(self):
		expression = FunctionExpression()

		self.file.give_character_back()
		self.tokenize(stop_ats=[opening_parenthesis_token], inheritable_give_back_stop_at=[opening_parenthesis_token], tree=expression)
		expression.convert_expression_to_name()

		self.tokenize(stop_ats=[closing_parenthesis_token], tree=expression)
		expression.convert_expressions_to_arguments()

		self.file.read_character() # absorb first "{"
		self.tokenize(stop_ats=[closing_bracket_token], tree=expression)

		return expression
	
	def read_conditional(self, buffer):
		expression = ConditionalExpression()
		self.file.give_character_back()
		if buffer == "else":
			buffer = buffer + " " + self.file.read_character() + self.file.read_character()
			if buffer != "else if":
				self.file.give_character_back()
				self.file.give_character_back()
				buffer = "else"
		
		expression.type = buffer

		if buffer != "else":
			self.file.read_character() # absorb first "("
			self.tokenize(stop_ats=[closing_parenthesis_token], tree=expression)
			expression.move_expressions()

		self.file.read_character() # absorb first "{"
		self.tokenize(stop_ats=[closing_bracket_token], tree=expression)

		return expression

	def read_variable_assignment(self, operator, left_hand, stop_ats):
		# keep reading until we absorb the full value (ended by semicolon)
		expression = VariableAssignmentExpression(operator, left_hand)
		self.tokenize(stop_ats=[semicolon_token] + stop_ats, give_back_stop_ats=[semicolon_token] + stop_ats, tree=expression)
		return expression
	
	def read_parentheses_expression(self):
		expression = ParenthesesExpression()
		self.tokenize(stop_ats=[closing_parenthesis_token], tree=expression)
		return expression
	
	def read_method_expression(self, method_name):
		expression = MethodExpression(method_name)
		self.tokenize(stop_ats=[closing_parenthesis_token], give_back_stop_ats=[semicolon_token], tree=expression)
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
			elif template_literal_token.match(char):
				if template_literal == None:
					template_literal = TemplateLiteral() # create template literal if we don't have one
				# tokenize b/c we're parsing runnable code
				self.tokenize(stop_ats=[template_literal_token], tree=template_literal)
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
	
	def read_chaining_expression(self, first_symbol_name, inheritable_give_back_stop_at):
		chaining_expression = ChainingExpression()
		self.add_expression(chaining_expression, self.get_symbol(first_symbol_name))
		try:
			self.file.give_character_back()
			while self.file.read_character() == ".":
				self.tokenize(stop_ats=[], give_back_stop_ats=inheritable_give_back_stop_at + [semicolon_token, chaining_token, operator_token_without_concatenation, closing_parenthesis_token], tree=chaining_expression)
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
				self.tokenize(stop_ats=[], give_back_stop_ats=inheritable_give_back_stop_at + [semicolon_token, namespace_token, operator_token_without_concatenation, closing_parenthesis_token], tree=namespace_expression)
			self.file.give_character_back()
			self.file.give_character_back()
		except:
			pass # if we hit an EOF, just ignore it
			
		return namespace_expression
	
	def read_operator(self):
		self.file.give_character_back()
		buffer = ""
		has_match = False
		for i in range(0, 5):
			buffer = buffer + self.file.read_character(ignore_whitespace=False)
			match = valid_operator.match(buffer)
			if match != None:
				has_match = True
			elif match == None and has_match and operator_token.match(buffer[-1]) == None:
				self.file.give_character_back()
				match = valid_operator.match(buffer[0:-1])
				return OperatorExpression(match.group(0))
		
		for i in range(0, 5):
			self.file.give_character_back()
		self.operator_ban = (self.file.current_line_index, self.file.current_index + 5)
		return None
	
	def get_symbol(self, symbol_name):
		if variable_token.match(symbol_name[0]):
			return VariableSymbol(symbol_name)
		else:
			return Symbol(symbol_name)
	
	def add_expression(self, tree, expression):
		tree.expressions.append(expression)
		expression.parent = tree
	
	def update_last_expression(self, tree, new_expression):
		self.add_expression(new_expression, tree.expressions.pop())

	def tokenize(self, stop_ats=[], give_back_stop_ats=[], buffer_give_back_stop_at=[], inheritable_give_back_stop_at=[], tree=None):
		self.buffer = ""
		while True:
			char = ''
			try:
				char = self.file.read_character()
			except:
				print("Finished file")
				break
			
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
				keywords.match(self.buffer)
				and keywords.match(self.buffer + char) == None
				and (
					valid_symbol.match(self.buffer + char) == None
					or self.file.skipped_space
				)
			):
				if valid_conditional.match(self.buffer): # handle conditionals
					self.add_expression(tree, self.read_conditional(self.buffer))
					self.buffer = ""
				elif valid_for.match(self.buffer): # handle for loops
					self.add_expression(tree, self.read_for_loop())
					self.buffer = ""
				elif valid_while.match(self.buffer): # handle while loops
					self.add_expression(tree, self.read_while_loop())
					self.buffer = ""
				elif valid_function.match(self.buffer): # handle functions
					self.add_expression(tree, self.read_function())
					self.buffer = ""
				elif valid_switch.match(self.buffer): # handle switch statements
					self.add_expression(tree, self.read_switch())
					self.buffer = ""
				elif valid_switch_string.match(self.buffer): # handle switch string statements
					self.add_expression(tree, self.read_switch())
					self.buffer = ""
				elif valid_case.match(self.buffer): # handle case statements
					self.add_expression(tree, self.read_case())
					self.buffer = ""
				elif valid_default.match(self.buffer): # handle default statement
					self.add_expression(tree, self.read_default())
					self.buffer = ""
				elif valid_package.match(self.buffer): # handle packages
					self.add_expression(tree, self.read_package())
					self.buffer = ""
				
				continue

			if (
				operator_token.match(char)
				and (
					operator_token_only_concatenation.match(char) == None
					or self.file.skipped_space == True
				)
				and (
					self.file.current_line_index > self.operator_ban[0]
					or self.file.current_index > self.operator_ban[1]
				)
			): # handle operators
				if comma_token.match(char): # handle commas in special case
					if type(tree) is MethodExpression:
						self.absorb_buffer(tree)
						tree.convert_expressions_to_arguments()
					elif type(tree) is FunctionExpression:
						self.absorb_buffer(tree)
						tree.convert_expressions_to_arguments()
				else:
					operator = self.read_operator()
					if operator != None:
						self.absorb_buffer(tree)
						if valid_comment.match(operator.operator):
							self.add_expression(tree, self.read_comment())
						elif valid_assignment.match(operator.operator):
							# take last expression and use that as left hand for variable assignment
							last_expression = tree.expressions.pop()
							new_expression = self.read_variable_assignment(operator, last_expression, stop_ats)
							last_expression.parent = new_expression
							self.add_expression(tree, new_expression)
						elif valid_postfix.match(operator.operator):
							# take last expression and use that for postfix operation
							last_expression = tree.expressions.pop()
							new_expression = PostfixExpression(last_expression, operator)
							last_expression.parent = new_expression
							self.add_expression(tree, new_expression)
						else:
							self.add_expression(tree, operator)
			elif chaining_token.match(char): # handle chaining (%test.test.test.test...)
				if valid_symbol.match(self.buffer):
					# if we have a valid symbol, then build chaining expression from remaining valid symbols
					self.add_expression(tree, self.read_chaining_expression(self.buffer, inheritable_give_back_stop_at))
					self.buffer = "" # absorb buffer
				else:
					raise TokenizerException(self, f"Invalid symbol for chain expression '{self.buffer}'")
			elif namespace_token.match(char): # handle namespaces ($Test::frog:egg...)
				if valid_symbol.match(self.buffer):
					# if we have a valid symbol, then build chaining expression from remaining valid symbols
					self.add_expression(tree, self.read_namespace_expression(self.buffer, inheritable_give_back_stop_at))
					self.buffer = "" # absorb buffer
				else:
					raise TokenizerException(self, f"Invalid symbol for namespace expression '{self.buffer}'")
			elif semicolon_token.match(char):
				# just absorb the character and move on, we have automatic semicolon placement
				self.absorb_buffer(tree)
			elif string_token.match(char): # handle strings
				string = self.read_string()
				self.add_expression(tree, string)
			elif parentheses_token.match(char):
				if opening_parenthesis_token.match(char) and valid_symbol.match(self.buffer) == None: # handle math parentheses
					self.add_expression(tree, self.read_parentheses_expression())
				elif opening_parenthesis_token.match(char) and valid_symbol.match(self.buffer) != None: # handle method parentheses
					self.add_expression(tree, self.read_method_expression(self.buffer))
			else: # when in doubt, add to buffer
				self.buffer = self.buffer + char
		return tree