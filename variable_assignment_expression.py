class VariableAssignmentExpression:
	def __init__(self, left_hand_expression):
		self.left_hand_expression = left_hand_expression
		self.expressions = []
	
	def __str__(self):
		return f"VariableAssignment({self.left_hand_expression}, {self.expressions})"
	
	def to_script(self):
		value = ""
		for expression in self.expressions:
			value = value + expression.to_script()

		if value == "":
			raise Exception(f"Could not find value for variable assignment '{self.left_hand_expression}'")

		return f"{self.left_hand_expression.to_script()} = {value};"
