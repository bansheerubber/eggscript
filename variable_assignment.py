class VariableAssignment:
	def __init__(self, name, value):
		self.name = name
		self.value = value
	
	def __str__(self):
		return f"VariableAssignment({self.name}, {self.value})"
	
	def to_script(self):
		return f"{self.name} = {self.value.to_script()};"
