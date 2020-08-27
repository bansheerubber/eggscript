from argument_expression import ArgumentExpression
from expression import Expression

class MethodExpression(Expression):
	def __init__(self, method_name):
		self.method_name = method_name
		self.expressions = []
		self.argument_expressions = []
		self.no_new_line = True # supress newlines TODO remove need for this
		self.parent = None
	
	def convert_expressions_to_arguments(self):
		if len(self.expressions) > 0:
			self.argument_expressions.append(ArgumentExpression(self.expressions))
			self.expressions = []
	
	def __str__(self):
		return f"MethodExpression({self.method_name}, {self.argument_expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		value = "  "
		for argument in self.argument_expressions:
			value = (value + argument.to_script() + ", ")

		return f"{self.method_name}({value[0:-2].strip()}){self.handle_semicolon()}"