from eggscript_src.config import get_config
from eggscript_src.expressions.expression import Expression
from eggscript_src.regex import closing_curly_bracket_token, closing_parenthesis_token, opening_curly_bracket_token, semicolon_token, valid_while

class WhileLoopExpression(Expression):
	def __init__(self, tokenizer=None):
		super().__init__(tokenizer=tokenizer)
		self.conditional_expressions = []
		self.is_code_block = True
	
	def convert_expressions_to_conditionals(self):
		self.conditional_expressions = self.expressions
		self.expressions = []
	
	def __str__(self):
		return f"WhileLoopExpression({self.conditional_expressions}, {self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		full_output = ""

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

		full_output = "while(" + output + ")" + space + "{" + newline
		
		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output + (tab * (self.get_indent_level() - 1)) + "}"

		return full_output
	
	def read_expression(tokenizer, tree):
		expression = WhileLoopExpression(tokenizer=tokenizer)
		
		tokenizer.tokenize(stop_ats=[closing_parenthesis_token], tree=expression)
		expression.convert_expressions_to_conditionals()

		tokenizer.tokenize(give_back_stop_ats=[opening_curly_bracket_token, semicolon_token], tree=expression)

		# figure out if this is a single line if-statement or not
		if tokenizer.file.read_character() == "{":
			tokenizer.tokenize(stop_ats=[closing_curly_bracket_token], tree=expression)
		else:
			tokenizer.file.give_character_back()

		return expression

Expression.add_keyword_regex(valid_while, WhileLoopExpression)