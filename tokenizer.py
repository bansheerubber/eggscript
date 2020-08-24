from chaining_expression import ChainingExpression
from file import File
from literal import Literal
from operator_expression import OperatorExpression
from template_literal import TemplateLiteral
from tokenizer_exception import TokenizerException
from regex import assignment_token, chaining_token, digits, operator_token, template_literal_token, semicolon, string_token, valid_symbol, variable_token
from symbol import Symbol
from variable_assignment_expression import VariableAssignmentExpression
from variable_symbol import VariableSymbol

class Tokenizer:
	def __init__(self, file):
		self.file = file
	
	def absorb_buffer(self, tree):
		if digits.match(self.buffer):
			tree.expressions.append(Literal(self.buffer))
			self.buffer = ""
		elif valid_symbol.match(self.buffer):
			tree.expressions.append(self.get_symbol(self.buffer))
			self.buffer = ""

	def read_variable_assignment(self, left_hand):
		# keep reading until we absorb the full value (ended by semicolon)
		expression = VariableAssignmentExpression(left_hand)
		self.tokenize(stop_ats=[semicolon], tree=expression)
		return expression

	def read_string(self):
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
			elif string_token.match(char): # find the last "/'
				has_ended = True
			else: # add to the value
				output[len(output) - 1] = output[len(output) - 1] + char

		if template_literal == None:
			return Literal(output[0])
		else:
			template_literal.strings = output
			return template_literal
	
	def build_chaining_expression(self, first_symbol_name):
		chaining_expression = ChainingExpression()
		chaining_expression.expressions.append(self.get_symbol(first_symbol_name))
		buffer = ""
		while buffer == "" or valid_symbol.match(buffer):
			buffer = buffer + self.file.read_character(ignore_whitespace=True)
			if chaining_token.match(buffer[-1]):
				chaining_expression.expressions.append(self.get_symbol(buffer[0:-1]))
				buffer = ""
		
		chaining_expression.expressions.append(self.get_symbol(buffer[0:-1]))
		self.file.give_character_back()
		return chaining_expression
	
	def get_symbol(self, symbol_name):
		if variable_token.match(symbol_name[0]):
			return VariableSymbol(symbol_name)
		else:
			return Symbol(symbol_name)

	def tokenize(self, stop_ats=[], tree=None):
		self.buffer = ""
		while True:
			char = ''
			try:
				char = self.file.read_character()
			except:
				print("Finished file")
				break
			
			for stop_at in stop_ats:
				if stop_at.match(char):
					self.absorb_buffer(tree)
					return tree

			if chaining_token.match(char): # handle chaining (%test.test.test.test...)
				if valid_symbol.match(self.buffer):
					# if we have a valid symbol, then build chaining expression from remaining valid symbols
					tree.expressions.append(self.build_chaining_expression(self.buffer))
					self.buffer = "" # absorb buffer
				else:
					raise TokenizerException(self, f"Invalid symbol '{self.buffer}'")
			elif assignment_token.match(char): # handle variable assignment
				self.absorb_buffer(tree)
				
				# take last expression and use that as left hand for variable assignment
				last_expression = tree.expressions.pop()
				tree.expressions.append(self.read_variable_assignment(last_expression))
			elif string_token.match(char): # handle strings
				string = self.read_string()
				tree.expressions.append(string)
			elif operator_token.match(char): # handle operators
				self.absorb_buffer(tree)
				tree.expressions.append(OperatorExpression(char))
			else: # when in doubt, add to buffer
				self.buffer = self.buffer + char
		return tree