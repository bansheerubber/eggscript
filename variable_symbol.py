class VariableSymbol:
	def __init__(self, name):
		self.name = name
	
	def __str__(self):
		return f"VariableSymbol({self.name})"
	
	def to_script(self):
		return self.name