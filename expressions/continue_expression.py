from expression import Expression
from regex import valid_continue

class ContinueExpression(Expression):
	def __init__(self):
		super().__init__()
	
	def __str__(self):
		return "ContinueExpression()"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		return f"continue{self.handle_semicolon()}"
	
	def read_expression(tokenizer, tree):
		tokenizer.file.give_character_back()
		return ContinueExpression()

Expression.add_keyword_regex(valid_continue, ContinueExpression)