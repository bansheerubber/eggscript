from eggscript_src.config import get_config
from eggscript_src.expressions.expression import Expression

class Comment(Expression):
	def __init__(self, comment, tokenizer=None):
		super().__init__(tokenizer=tokenizer)
		self.comment = comment
		self.parent = None
	
	def __str__(self):
		return f"Comment({self.comment})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		if get_config("nocomments") != True and self.parent.is_code_block == False:
			return self.comment + "\n"
		else:
			return self.comment
	
	def read_expression(tokenizer):
		while tokenizer.file.give_character_back() != "/":
			pass
		tokenizer.file.give_character_back()
			
		# read the rest of the line
		comment = tokenizer.file.absorb_line()
		return Comment(comment, tokenizer=tokenizer)