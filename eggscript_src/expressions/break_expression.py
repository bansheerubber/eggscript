from eggscript_src.expressions.expression import Expression
from eggscript_src.regex import valid_break

class BreakExpression(Expression):
	def __init__(self, tokenizer=None):
		super().__init__(tokenizer=tokenizer)
	
	def __str__(self):
		return "BreakExpression()"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		return f"break{self.handle_semicolon()}"

	def read_expression(tokenizer, tree):
		tokenizer.file.give_character_back()
		return BreakExpression(tokenizer=tokenizer)

Expression.add_keyword_regex(valid_break, BreakExpression)