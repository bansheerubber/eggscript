from config import get_config
from expression import Expression

class CaseExpression(Expression):
	def __init__(self):
		self.expressions = []
		self.conditional_expressions = []
		self.code_block = True
	
	def convert_expressions_to_conditionals(self):
		self.conditional_expressions = self.expressions
		self.expressions = []
	
	def __str__(self):
		return f"CaseExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		newline = "\n"
		space = " "
		tab = "\t"
		if get_config("minify") == True:
			newline = ""
			space = ""
			tab = ""

		output = ""
		for conditional_expression in self.conditional_expressions:
			output = output + conditional_expression.to_script()
		
		full_output = f"case {output}:" + newline

		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output
	
		return full_output