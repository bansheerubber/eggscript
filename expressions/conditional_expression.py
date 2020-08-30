from config import get_config
from expression import Expression
from regex import closing_curly_bracket_token, closing_parenthesis_token, opening_curly_bracket_token, semicolon_token, valid_conditional

class ConditionalExpression(Expression):
	def __init__(self):
		super().__init__()
		self.conditional_expressions = []
		self.is_code_block = True
		self.type = ""
	
	def __str__(self):
		return f"ConditionalExpression({self.type}, {self.conditional_expressions}, {self.expressions})"
	
	def __repr__(self):
		return self.__str__()

	def move_expressions(self):
		self.conditional_expressions = self.expressions
		self.expressions = []
	
	def to_script(self):
		full_output = ""

		newline = "\n"
		space = " "
		tab = "\t"
		if get_config("minify") == True:
			newline = ""
			space = ""
			tab = ""
		
		if self.type != "else":
			output = ""
			for conditional_expression in self.conditional_expressions:
				output = output + conditional_expression.to_script()
			
			full_output = self.type + "(" + output + ")" + space + "{" + newline
		else:
			full_output = self.type + space + "{" + newline
		
		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output + (tab * (self.get_indent_level() - 1)) + "}"

		return full_output
	
	def read_expression(tokenizer, tree):
		expression = ConditionalExpression()
		tokenizer.file.give_character_back()
		if tokenizer.buffer == "else":
			tokenizer.buffer = tokenizer.buffer + " " + tokenizer.file.read_character() + tokenizer.file.read_character()
			if tokenizer.buffer != "else if":
				tokenizer.file.give_character_back(ignore_whitespace=True)
				tokenizer.file.give_character_back(ignore_whitespace=True)

				tokenizer.buffer = "else"
		
		expression.type = tokenizer.buffer

		if tokenizer.buffer != "else":
			tokenizer.file.read_character() # absorb first "("
			tokenizer.tokenize(stop_ats=[closing_parenthesis_token], tree=expression)
			expression.move_expressions()

		tokenizer.tokenize(give_back_stop_ats=[opening_curly_bracket_token, semicolon_token], tree=expression)

		# figure out if this is a single line if-statement or not
		if tokenizer.file.read_character() == "{":
			tokenizer.tokenize(stop_ats=[closing_curly_bracket_token], tree=expression)
		else:
			tokenizer.file.give_character_back()

		return expression

Expression.add_keyword_regex(valid_conditional, ConditionalExpression)