from eggscript_src.expressions.expression import Expression
from eggscript_src.regex import closing_parenthesis_token
from eggscript_src.syntax_exception import SyntaxException

class ParenthesesExpression(Expression):
	def __init__(self, tokenizer=None):
		super().__init__(tokenizer=tokenizer)
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
			raise SyntaxException(self, "Parentheses syntax error: empty expression")

		return f"({value})"
	
	def read_expression(tokenizer, vector_mode=False):
		expression = ParenthesesExpression(tokenizer=tokenizer)
		tokenizer.tokenize(stop_ats=[closing_parenthesis_token], tree=expression, vector_mode=vector_mode)
		return expression