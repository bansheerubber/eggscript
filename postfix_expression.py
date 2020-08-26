class PostfixExpression:
	def __init__(self, expression, operator):
		self.expression = expression
		self.operator = operator
	
	def __str__(self):
		return f"PostfixExpression({self.expression, self.operator})"

	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		semicolon = ""
		if hasattr(self.parent, "code_block"):
			semicolon = ";"

		return f"{self.expression.to_script()}{self.operator.to_script().strip()}{semicolon}"