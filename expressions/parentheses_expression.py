from expression import Expression
from regex import closing_parenthesis_token

class ParenthesesExpression(Expression):
	def __init__(self):
		super().__init__()
		self.parent = None
		self.is_chainable = True
	
	def __str__(self):
		return f"ParenthesesExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		value = ""
		for expression in self.expressions:
			value = value + expression.to_script()

		if value == "":
			return f"(((({value}))))"

		return f"({value})"
	
	def read_expression(tokenizer):
		expression = ParenthesesExpression()
		tokenizer.tokenize(stop_ats=[closing_parenthesis_token], tree=expression)
		return expression