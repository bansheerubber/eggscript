from config import get_config
from expression import Expression

class DefaultExpression(Expression):
	def __init__(self):
		super().__init__()
		self.code_block = True
	
	def __str__(self):
		return f"DefaultExpression()"
	
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

		full_output = f"default:" + newline

		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output
	
		return full_output