class ChainingExpression:
	def __init__(self):
		self.expressions = []
	
	def __str__(self):
		return f"ChainingExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		output = ""
		for expression in self.expressions:
			output = output + expression.to_script() + "."
		return output[0:-1]