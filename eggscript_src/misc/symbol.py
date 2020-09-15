from eggscript_src.expressions.expression import Expression

class Symbol(Expression):
	def __init__(self, name):
		super().__init__(no_errors=True)
		self.name = name
		self.parent = None
	
	def __str__(self):
		return f"Symbol({self.name})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		return self.name