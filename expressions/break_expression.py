from expression import Expression

class BreakExpression(Expression):
	def __init__(self):
		super().__init__()
	
	def __str__(self):
		return "BreakExpression()"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		return f"break{self.handle_semicolon()}"