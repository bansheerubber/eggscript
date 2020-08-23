from file import File
from literal import Literal
from operator_expression import OperatorExpression
from template_literal import TemplateLiteral
from regex import digits, operator_token, template_literal_token, semicolon, string_token, valid_variable_name, variable_token
from variable import Variable
from variable_assignment import VariableAssignment

class Tokenizer:
	def __init__(self, file):
		self.file = file
	
	def dump_buffer(self, tree):
		if digits.match(self.buffer):
			tree.expressions.append(Literal(self.buffer))
			self.buffer = ""
	
	def read_variable_name(self):
		# keep reading until we absorb the full variable
		self.file.give_character_back()
		variable_name = self.file.read_character()
		while valid_variable_name.fullmatch(variable_name) or len(variable_name) == 1:
			char = self.file.read_character()
			variable_name = variable_name + char
		self.file.give_character_back()
		return variable_name[0:-1]

	def read_variable_assignment(self, stop_ats):
		variable_name = self.read_variable_name()

		# absorb equals sign
		char = self.file.read_character()
		for stop_at in stop_ats:
			if stop_at.match(char):
				print(f"TODO: Shouldn't be finding normal variable '{variable_name}' in variable assignment")
				return Variable(variable_name)

		if char != "=":
			print(f"TODO: Shouldn't be finding normal variable '{variable_name}' in variable assignment (failed when found '{char}' instead of '=')")
			return Variable(variable_name)
		
		# keep reading until we absorb the full value (ended by semicolon)
		variable_assignment = VariableAssignment(variable_name)
		self.tokenize(stop_ats=stop_ats + [semicolon], state=0b100, tree=variable_assignment)
		return variable_assignment

	def read_string(self):
		has_ended = False
		output = ['']
		template_literal = None
		while has_ended == False:
			char = self.file.read_character(ignore_whitespace=False)
			# if we read a backslash, imeditally read the next character so we don't trip up on \" or \'
			if char == "\\":
				output[len(output) - 1] = output[len(output) - 1] + char + self.file.read_character(ignore_whitespace=False)
				continue
			elif template_literal_token.match(char):
				if template_literal == None:
					template_literal = TemplateLiteral()
				self.tokenize(stop_ats=[template_literal_token], state=0b100, tree=template_literal)
				template_literal.add_template()
				output.append('')
			elif string_token.match(char):
				has_ended = True
			else:
				output[len(output) - 1] = output[len(output) - 1] + char

		if template_literal == None:
			return Literal(output[0])
		else:
			template_literal.strings = output
			return template_literal
		
	'''
	state bitmask

	1st: we're in neutral state (waiting for variable assignment, method call, etc)
	2st: stop after we have first tree value
	3nd: general expression
	'''
	def tokenize(self, stop_ats=[], state=0b1, tree=None):
		self.buffer = ""
		while True:
			if tree != None and state & 0b10:
				return tree
			
			char = ''
			try:
				char = self.file.read_character()
			except:
				print("Finished file")
				break
				
			for stop_at in stop_ats:
				if stop_at.match(char):
					# special cases when we hit a stop character
					if digits.match(self.buffer) and state & 0b100:
						self.dump_buffer(tree)
						return tree
					else:
						return tree

			# we're dealing with a variable assignment
			if variable_token.match(char) and state & 0b1:
				variable_assignment = self.read_variable_assignment(stop_ats)
				if tree != None:
					tree.expressions.append(variable_assignment)
				elif state & 0b10:
					return variable_assignment
			# we're dealing with a string during general expression
			elif string_token.match(char) and state & 0b100:
				string = self.read_string()
				tree.expressions.append(string)
			# we're dealing with a variable reference during general expression
			elif variable_token.match(char) and state & 0b100:
				tree.expressions.append(Variable(self.read_variable_name()))
			# we're dealing with operators
			elif operator_token.match(char) and state & 0b100:
				self.dump_buffer(tree)
				tree.expressions.append(OperatorExpression(char))
			else:
				self.buffer = self.buffer + char
		return tree