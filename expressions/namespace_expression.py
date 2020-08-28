from expression import Expression

class NamespaceExpression(Expression):
	def __init__(self):
		self.expressions = []
		self.parent = None
		self.is_chainable = True
	
	def __str__(self):
		return f"NamespaceExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		output = ""
		for expression in self.expressions:
			output = output + expression.to_script() + "::"

		return output[0:-2] + self.handle_semicolon()