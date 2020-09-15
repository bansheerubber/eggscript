from eggscript_src.expressions.expression import Expression

class ArgumentExpression(Expression):
	def __init__(self, expressions=[], tokenizer=None, current_line_index=None, current_index=None, current_file_name=None):
		super().__init__(expressions=expressions, tokenizer=tokenizer, current_line_index=current_line_index, current_index=current_index, current_file_name=current_file_name)
	
	def __str__(self):
		return f"ArgumentExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		output = ""
		for expression in self.expressions:
			output = output + expression.to_script()
		return output