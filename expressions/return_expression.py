from expression import Expression
from regex import semicolon_token, valid_return

class ReturnExpression(Expression):
	def __init__(self):
		super().__init__()
	
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
	
	def read_expression(tokenizer):
		expression = ReturnExpression()
		
		tokenizer.file.give_character_back()
		tokenizer.tokenize(give_back_stop_ats=[semicolon_token], tree=expression)
		return expression

Expression.add_keyword_regex(valid_return, ReturnExpression)