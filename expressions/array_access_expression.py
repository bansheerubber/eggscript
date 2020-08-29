from argument_expression import ArgumentExpression
from config import get_config
from expression import Expression
import re

class ArrayAccessExpression(Expression):
	def __init__(self, symbol):
		super().__init__()
		self.symbol = symbol
		self.argument_expressions = []
		self.parent = None
		self.has_arguments = True
	
	def convert_expressions_to_arguments(self):
		if len(self.expressions) > 0:
			self.argument_expressions.append(ArgumentExpression(expressions=self.expressions))
			self.expressions = []
	
	def __str__(self):
		return f"ArrayAccessExpression({self.symbol}, {self.argument_expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		space = " "
		if get_config("minify") == True:
			space = ""
		
		value = "  "
		for argument in self.argument_expressions:
			value = (value + argument.to_script() + "," + space)

		return f"{self.symbol.to_script()}[{re.sub(r',$', '', value.strip())}]{self.handle_semicolon()}"