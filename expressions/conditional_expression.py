from config import get_config
from expression import Expression

class ConditionalExpression(Expression):
	def __init__(self):
		super().__init__()
		self.conditional_expressions = []
		self.code_block = True
		self.type = ""
	
	def __str__(self):
		return f"ConditionalExpression({self.type}, {self.conditional_expressions}, {self.expressions})"
	
	def __repr__(self):
		return self.__str__()

	def move_expressions(self):
		self.conditional_expressions = self.expressions
		self.expressions = []
	
	def to_script(self):
		full_output = ""

		newline = "\n"
		space = " "
		tab = "\t"
		if get_config("minify") == True:
			newline = ""
			space = ""
			tab = ""
		
		if self.type != "else":
			output = ""
			for conditional_expression in self.conditional_expressions:
				output = output + conditional_expression.to_script()
			
			full_output = self.type + "(" + output + ")" + space + "{" + newline
		else:
			full_output = self.type + space + "{" + newline
		
		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output + (tab * (self.get_indent_level() - 1)) + "}"

		return full_output