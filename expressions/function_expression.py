from config import get_config
from argument_expression import ArgumentExpression
from expression import Expression
from regex import closing_curly_bracket_token, closing_parenthesis_token, opening_parenthesis_token, valid_function
import re

class FunctionExpression(Expression):
	def __init__(self):
		super().__init__()
		self.name_symbol = None
		self.argument_expressions = []
		self.parent = None
		self.is_code_block = True
		self.has_arguments = True
	
	def convert_expression_to_name(self):
		self.name_symbol = self.expressions[0]
		self.expressions = []

	def convert_expressions_to_arguments(self):
		if len(self.expressions) > 0:
			self.argument_expressions.append(ArgumentExpression(expressions=self.expressions))
			self.expressions = []
	
	def __str__(self):
		return f"FunctionExpression({self.name_symbol}, {self.argument_expressions}, {self.expressions})"
	
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
		
		output = "  "
		for argument_expression in self.argument_expressions:
			output = output + argument_expression.to_script() + "," + space
		
		full_output = "function " + self.name_symbol.to_script() + "(" + re.sub(r',$', '', output.strip()) + ")" + space + "{" + newline
		
		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output + (tab * (self.get_indent_level() - 1)) + "}"

		return full_output
	
	def read_expression(tokenizer):
		expression = FunctionExpression()

		tokenizer.file.give_character_back()
		tokenizer.tokenize(stop_ats=[opening_parenthesis_token], inheritable_give_back_stop_at=[opening_parenthesis_token], tree=expression)
		expression.convert_expression_to_name()

		tokenizer.tokenize(stop_ats=[closing_parenthesis_token], tree=expression)
		expression.convert_expressions_to_arguments()

		tokenizer.file.read_character() # absorb first "{"
		tokenizer.tokenize(stop_ats=[closing_curly_bracket_token], tree=expression)

		return expression

Expression.add_keyword_regex(valid_function, FunctionExpression)