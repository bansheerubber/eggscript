from expression import Expression

class ArgumentExpression(Expression):
	def __init__(self, expressions=[]):
		super().__init__(expressions=expressions)
	
	def __str__(self):
		return f"ArgumentExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		output = ""
		for expression in self.expressions:
			output = output + expression.to_script()
		return output