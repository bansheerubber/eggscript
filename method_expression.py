from container_expression import ContainerExpression
from expression import Expression

class MethodExpression(Expression):
	def __init__(self, method_name):
		self.method_name = method_name
		self.expressions = []
		self.arguments = []
		self.no_new_line = True # supress newlines TODO remove need for this
		self.parent = None
	
	def convert_expressions_to_arguments(self):
		self.arguments.append(ContainerExpression(self.expressions))
		self.expressions = []
	
	def __str__(self):
		return f"MethodExpression({self.method_name}, {self.arguments})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		value = "  "
		for argument in self.arguments:
			value = (value + argument.to_script() + ", ")

		return f"{self.method_name}({value[0:-2].strip()}){self.handle_semicolon()}"