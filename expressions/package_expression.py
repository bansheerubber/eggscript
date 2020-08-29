from config import get_config
from expression import Expression
from regex import closing_curly_bracket_token, opening_curly_bracket_token, valid_package

class PackageExpression(Expression):
	def __init__(self):
		super().__init__()
		self.name_symbol = None
		self.is_code_block = True
	
	def convert_expression_to_name(self):
		self.name_symbol = self.expressions[0]
		self.expressions = []
	
	def __str__(self):
		return f"PackageExpression({self.name_symbol}, {self.expressions})"
	
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

		full_output = "package " + self.name_symbol.to_script() + space + "{" + newline
		
		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output + (tab * (self.get_indent_level() - 1)) + "};"

		return full_output
	
	def read_expression(tokenizer):
		expression = PackageExpression()

		tokenizer.file.give_character_back()

		tokenizer.tokenize(stop_ats=[opening_curly_bracket_token], tree=expression)
		expression.convert_expression_to_name()

		tokenizer.tokenize(stop_ats=[closing_curly_bracket_token], tree=expression)

		return expression

Expression.add_keyword_regex(valid_package, PackageExpression)