class OperatorExpression:
	def __init__(self, operator):
		self.operator = operator
	
	def __str__(self):
		return f"Operator({operator})"
	
	def to_script(self):
		return f"{self.operator}"