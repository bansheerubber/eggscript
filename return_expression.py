from expression import Expression

class ReturnExpression(Expression):
	def __init__(self):
		self.expressions = []
	
	def __str__(self):
		return f"ReturnExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		output = " "
		for expression in self.expressions:
			output = output + expression.to_script()
		
		if output == " ":
			output = ""

		return f"return{output}{self.handle_semicolon()}"