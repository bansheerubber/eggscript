from argument_expression import ArgumentExpression
from config import get_config
from expression import Expression
from regex import closing_curly_bracket_token, closing_parenthesis_token, opening_curly_bracket_token, opening_parenthesis_token, semicolon_token,valid_new

class NewObjectExpression(Expression):
	def __init__(self):
		super().__init__()
		self.class_expressions = None
		self.argument_expressions = []
		self.is_code_block = True
		self.has_arguments = True
		self.no_keywords_in_code_block = True
	
	def convert_expressions_to_class(self):
		self.class_expressions = self.expressions
		self.expressions = []
	
	def convert_expressions_to_arguments(self):
		if len(self.expressions) > 0:
			self.argument_expressions.append(ArgumentExpression(expressions=self.expressions))
			self.expressions = []
	
	def __str__(self):
		return f"NewObjectExpression({self.class_expressions}, {self.expressions})"
	
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
		for class_expression in self.class_expressions:
			output = output + class_expression.to_script()
		
		full_output = "new " + output

		output = ""
		for argument_expression in self.argument_expressions:
			output = output + argument_expression.to_script()

		full_output = full_output + "(" + output + ")"
		
		if len(self.expressions) > 0:
			output = ""
			for expression in self.expressions:
				output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
			
			full_output = full_output + space + "{" + newline + output + (tab * (self.get_indent_level() - 1)) + "}"

		return full_output + self.handle_semicolon()
	
	def read_expression(tokenizer, tree):
		expression = NewObjectExpression()
		tokenizer.file.give_character_back()

		tokenizer.tokenize(stop_ats=[opening_parenthesis_token], tree=expression)
		expression.convert_expressions_to_class()

		tokenizer.tokenize(stop_ats=[closing_parenthesis_token], tree=expression)
		expression.convert_expressions_to_arguments()

		tokenizer.tokenize(give_back_stop_ats=[opening_curly_bracket_token, semicolon_token], tree=expression)
		char = tokenizer.file.read_character() # absorb first "{"
		if opening_curly_bracket_token.match(char):
			tokenizer.tokenize(stop_ats=[closing_curly_bracket_token], tree=expression)
		else:
			tokenizer.file.give_character_back()

		return expression

Expression.add_keyword_regex(valid_new, NewObjectExpression)