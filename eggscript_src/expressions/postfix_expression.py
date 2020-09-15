from eggscript_src.expressions.expression import Expression

class PostfixExpression(Expression):
	def __init__(self, expression, operator, tokenizer=None):
		super().__init__(tokenizer=tokenizer)
		self.expression = expression
		self.operator = operator
	
	def __str__(self):
		return f"PostfixExpression({self.expression, self.operator})"

	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		return f"{self.expression.to_script()}{self.operator.to_script().strip()}{self.handle_semicolon()}"