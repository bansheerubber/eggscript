from eggscript_src.expressions.parentheses_expression import ParenthesesExpression
from eggscript_src.regex import vector_escape_token

class VectorEscapeExpression(ParenthesesExpression):
	def __init__(self, tokenizer=None):
		super().__init__(tokenizer=tokenizer)
		is_chainable = False
	
	def __str__(self):
		return f"VectorEscapeExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def read_expression(tokenizer):
		expression = VectorEscapeExpression(tokenizer=tokenizer)
		tokenizer.tokenize(stop_ats=[vector_escape_token], tree=expression)
		return expression