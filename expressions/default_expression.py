from config import get_config
from expression import Expression
from regex import closing_curly_bracket_token, valid_case, valid_default

class DefaultExpression(Expression):
	def __init__(self, tokenizer=None):
		super().__init__(tokenizer=tokenizer)
		self.is_code_block = True
	
	def __str__(self):
		return f"DefaultExpression()"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		newline = "\n"
		space = " "
		tab = "\t"
		if get_config("minify") == True:
			newline = ""
			space = ""
			tab = ""

		full_output = f"default:" + newline

		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output
	
		return full_output
	
	def read_expression(tokenizer, tree):
		expression = DefaultExpression(tokenizer=tokenizer)
		# read up until next case, next default, or }
		tokenizer.tokenize(give_back_stop_ats=[closing_curly_bracket_token], buffer_give_back_stop_at=[valid_case, valid_default], tree=expression)

		return expression

Expression.add_keyword_regex(valid_default, DefaultExpression)