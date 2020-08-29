from config import get_config
from expression import Expression
from inheritance_expression import InheritanceExpression
from regex import closing_curly_bracket_token, closing_parenthesis_token, colon_token, opening_parenthesis_token, valid_datablock

class DatablockExpression(Expression):
	def __init__(self):
		super().__init__()
		self.class_symbol = None
		self.name_symbol = None
		self.is_code_block = True
		self.no_keywords_in_code_block = True
	
	def convert_expression_to_class(self):
		self.class_symbol = self.expressions[0]
		self.expressions = []

	def convert_expression_to_name(self, expression=None):
		if expression == None:
			self.name_symbol = self.expressions[0]
		else:
			self.name_symbol = expression
		
		self.expressions = []
	
	def __str__(self):
		return f"DatablockExpression({self.class_symbol}, {self.name_symbol} {self.expressions})"
	
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

		full_output = "datablock " + self.class_symbol.to_script() + "(" + self.name_symbol.to_script() + ")" + space + "{" + newline
		
		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output + (tab * (self.get_indent_level() - 1)) + "};"

		return full_output
	
	def read_expression(tokenizer):
		expression = DatablockExpression()
		tokenizer.file.give_character_back()

		tokenizer.tokenize(stop_ats=[opening_parenthesis_token], tree=expression)
		expression.convert_expression_to_class()

		tokenizer.tokenize(stop_ats=[closing_parenthesis_token], give_back_stop_ats=[colon_token], tree=expression)

		if tokenizer.file.read_character() == ":":
			inheritance_expression = InheritanceExpression()
			inheritance_expression.child_class = expression.expressions[0]
			tokenizer.tokenize(stop_ats=[closing_parenthesis_token], tree=inheritance_expression)
			inheritance_expression.convert_expression_to_super_class()

			expression.convert_expression_to_name(expression=inheritance_expression)
		else:
			expression.convert_expression_to_name()
			tokenizer.file.give_character_back()

		tokenizer.file.read_character() # absorb first "{"
		tokenizer.tokenize(stop_ats=[closing_curly_bracket_token], tree=expression)

		return expression

Expression.add_keyword_regex(valid_datablock, DatablockExpression)