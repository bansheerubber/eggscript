class ParenthesesExpression:
	def __init__(self):
		self.expressions = []
		self.parent = None
	
	def __str__(self):
		return f"ParenthesesExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		value = ""
		for expression in self.expressions:
			value = value + expression.to_script()

		if value == "":
			raise Exception(f"Could not find value for variable assignment '{self.expressions}'")

		return f"({value})"