from expression import Expression

class ContinueExpression(Expression):
	def __init__(self):
		self.expressions = []
	
	def __str__(self):
		return "ContinueExpression()"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		return f"continue{self.handle_semicolon()}"