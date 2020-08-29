from config import get_config
from expression import Expression
from regex import closing_curly_bracket_token, closing_parenthesis_token, valid_switch, valid_switch_string

class SwitchExpression(Expression):
	def __init__(self, type):
		super().__init__()
		self.conditional_expressions = []
		self.type = type
		self.is_code_block = True
	
	def convert_expressions_to_conditionals(self):
		self.conditional_expressions = self.expressions
		self.expressions = []
	
	def __str__(self):
		return f"SwitchExpression({self.conditional_expressions}, {self.expressions})"
	
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

		full_output = self.type + "(" + output + ")" + space + "{" + newline
		
		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output + (tab * (self.get_indent_level() - 1)) + "}"

		return full_output
	
	def read_expression(tokenizer):
		tokenizer.file.give_character_back()
		tokenizer.file.give_character_back()
		char = tokenizer.file.read_character()
		switch_type = "switch"
		if char == "$":
			switch_type = "switch$"
		tokenizer.file.read_character()
		
		expression = SwitchExpression(switch_type)
		
		tokenizer.tokenize(stop_ats=[closing_parenthesis_token], tree=expression)
		expression.convert_expressions_to_conditionals()

		tokenizer.file.read_character() # absorb first "{"
		tokenizer.tokenize(stop_ats=[closing_curly_bracket_token], tree=expression)

		return expression

Expression.add_keyword_regex(valid_switch, SwitchExpression)
Expression.add_keyword_regex(valid_switch_string, SwitchExpression)