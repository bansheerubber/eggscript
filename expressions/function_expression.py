from config import get_config
from argument_expression import ArgumentExpression
from expression import Expression
import re

class FunctionExpression(Expression):
	def __init__(self):
		super().__init__()
		self.name_symbol = None
		self.argument_expressions = []
		self.parent = None
		self.code_block = True
	
	def convert_expression_to_name(self):
		self.name_symbol = self.expressions[0]
		self.expressions = []

	def convert_expressions_to_arguments(self):
		if len(self.expressions) > 0:
			self.argument_expressions.append(ArgumentExpression(expressions=self.expressions))
			self.expressions = []
	
	def __str__(self):
		return f"FunctionExpression({self.name_symbol}, {self.argument_expressions}, {self.expressions})"
	
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
		
		output = "  "
		for argument_expression in self.argument_expressions:
			output = output + argument_expression.to_script() + "," + space
		
		full_output = "function " + self.name_symbol.to_script() + "(" + re.sub(r',$', '', output.strip()) + ")" + space + "{" + newline
		
		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output + (tab * (self.get_indent_level() - 1)) + "}"

		return full_output