class VariableAssignment:
	def __init__(self, name):
		self.name = name
		self.expressions = []
	
	def __str__(self):
		return f"VariableAssignment({self.name}, {self.expressions})"
	
	def to_script(self):
		value = ""
		for expression in self.expressions:
			value = value + expression.to_script()

		if value == "":
			value = "$FixMe"

		return f"{self.name} = {value};"
