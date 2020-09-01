from parentheses_expression import ParenthesesExpression
from regex import vector_escape_token

class VectorEscapeExpression(ParenthesesExpression):
	def __init__(self):
		super().__init__()
		is_chainable = False
	
	def read_expression(tokenizer):
		expression = VectorEscapeExpression()
		tokenizer.tokenize(stop_ats=[vector_escape_token], tree=expression)
		return expression