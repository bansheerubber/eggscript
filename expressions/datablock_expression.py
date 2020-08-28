from config import get_config
from expression import Expression

class DatablockExpression(Expression):
	def __init__(self):
		super().__init__()
		self.class_symbol = None
		self.name_symbol = None
		self.code_block = True
	
	def convert_expression_to_class(self):
		self.class_symbol = self.expressions[0]
		self.expressions = []

	def convert_expression_to_name(self, expression=None):
		if expression == None:
			self.name_symbol = self.expressions[0]
		else:
			self.name_symbol = expression
		
		self.expressions = []
	
	def __str__(self):
		return f"DatablockExpression({self.class_symbol}, {self.name_symbol} {self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		full_output = ""

		newline = "\n"
		space = " "
		tab = "\t"
		if get_config("minify") == True:
			newline = ""
			space = ""
			tab = ""

		full_output = "datablock " + self.class_symbol.to_script() + "(" + self.name_symbol.to_script() + ")" + space + "{" + newline
		
		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output + (tab * (self.get_indent_level() - 1)) + "};"

		return full_output