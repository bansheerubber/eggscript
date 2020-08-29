from config import get_config
from expression import Expression
from regex import closing_curly_bracket_token, colon_token, valid_case, valid_default

class CaseExpression(Expression):
	def __init__(self):
		super().__init__()
		self.conditional_expressions = []
		self.is_code_block = True
	
	def convert_expressions_to_conditionals(self):
		self.conditional_expressions = self.expressions
		self.expressions = []
	
	def __str__(self):
		return f"CaseExpression({self.expressions})"
	
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

		output = ""
		for conditional_expression in self.conditional_expressions:
			output = output + conditional_expression.to_script()
		
		full_output = f"case {output}:" + newline

		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output
	
		return full_output
	
	def read_expression(tokenizer):
		expression = CaseExpression()
		tokenizer.file.give_character_back()
		tokenizer.tokenize(stop_ats=[colon_token], tree=expression)
		expression.convert_expressions_to_conditionals()

		# read up until next case, next default, or }
		tokenizer.tokenize(give_back_stop_ats=[closing_curly_bracket_token], buffer_give_back_stop_at=[valid_case, valid_default], tree=expression)

		return expression

Expression.add_keyword_regex(valid_case, CaseExpression)