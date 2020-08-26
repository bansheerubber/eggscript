class MethodExpression:
	def __init__(self, method_name):
		self.method_name = method_name
		self.expressions = []
		self.arguments = []
		self.no_new_line = True # supress newlines TODO remove need for this
		self.parent = None
	
	def convert_expressions_to_arguments(self):
		for expression in self.expressions:
			self.arguments.append(expression)
		self.expressions = []
	
	def __str__(self):
		return f"MethodExpression({self.method_name}, {self.arguments})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		value = "  "
		for argument in self.arguments:
			value = (value + argument.to_script() + ", ")
		
		semicolon = ""
		if hasattr(self.parent, "code_block"):
			semicolon = ";"

		return f"{self.method_name}({value[0:-2].strip()}){semicolon}"