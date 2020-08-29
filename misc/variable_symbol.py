from expression import Expression

class VariableSymbol(Expression):
	def __init__(self, name):
		super().__init__()
		self.name = name
		self.parent = None
	
	def __str__(self):
		return f"VariableSymbol({self.name})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		return self.name