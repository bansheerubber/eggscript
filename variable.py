class Variable:
	def __init__(self, name):
		self.name = name
	
	def __str__(self):
		return f"Variable({self.name})"
	
	def to_script(self):
		return self.name