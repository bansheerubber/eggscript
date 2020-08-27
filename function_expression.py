from argument_expression import ArgumentExpression
from expression import Expression

class FunctionExpression(Expression):
	def __init__(self):
		self.name_symbol = None
		self.expressions = []
		self.argument_expressions = []
		self.parent = None
	
	def convert_expression_to_name(self):
		self.name_symbol = self.expressions[0]
		self.expressions = []

	def convert_expressions_to_arguments(self):
		if len(self.expressions) > 0:
			self.argument_expressions.append(ArgumentExpression(self.expressions))
			self.expressions = []
	
	def __str__(self):
		return f"FunctionExpression({self.name_symbol}, {self.argument_expressions}, {self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		full_output = ""
		
		output = "  "
		for argument_expression in self.argument_expressions:
			output = output + argument_expression.to_script() + ", "
		
		full_output = "function " + self.name_symbol.to_script() + "(" + output[0:-2].strip() + ") {\n"
		
		output = ""
		for expression in self.expressions:
			output = output + ("\t" * self.get_indent_level()) + expression.to_script() + "\n"
		
		full_output = full_output + output[0:-1] + "\n" + ("\t" * (self.get_indent_level() - 1)) + "}"

		return full_output