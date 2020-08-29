from expression import Expression
from regex import valid_break

class BreakExpression(Expression):
	def __init__(self):
		super().__init__()
	
	def __str__(self):
		return "BreakExpression()"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		return f"break{self.handle_semicolon()}"

	def read_expression(tokenizer):
		tokenizer.file.give_character_back()
		return BreakExpression()

Expression.add_keyword_regex(valid_break, BreakExpression)