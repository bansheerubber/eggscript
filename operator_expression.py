class OperatorExpression:
	def __init__(self, operator):
		self.operator = operator
	
	def __str__(self):
		return f"Operator({self.operator})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		return f"{self.operator}"