from expression import Expression
from regex import chaining_token, closing_bracket_token, closing_parenthesis_token, namespace_token, operator_token_without_concatenation, semicolon_token, template_literal_token

class NamespaceExpression(Expression):
	def __init__(self):
		super().__init__()
		self.parent = None
		self.is_chainable = True
	
	def __str__(self):
		return f"NamespaceExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		output = ""
		for expression in self.expressions:
			output = output + expression.to_script() + "::"

		return output[0:-2] + self.handle_semicolon()
	
	def read_expression(tokenizer, inheritable_give_back_stop_at):
		namespace_expression = NamespaceExpression()
		tokenizer.add_expression(namespace_expression, tokenizer.get_symbol(tokenizer.buffer))
		tokenizer.file.give_character_back()
		while tokenizer.file.read_character() == ":" and tokenizer.file.read_character() == ":":
			tokenizer.tokenize(stop_ats=[], give_back_stop_ats=inheritable_give_back_stop_at + [semicolon_token, namespace_token, operator_token_without_concatenation, closing_parenthesis_token, closing_bracket_token, chaining_token, template_literal_token], tree=namespace_expression)
		tokenizer.file.give_character_back()
			
		return namespace_expression