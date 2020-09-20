from eggscript_src.expressions.expression import Expression
from eggscript_src.regex import chaining_token, closing_bracket_token, closing_parenthesis_token, namespace_token, operator_token_without_concatenation, semicolon_token, template_literal_token, vector_cross_token, valid_start_of_symbol, whitespace

class NamespaceExpression(Expression):
	def __init__(self, tokenizer=None):
		super().__init__(tokenizer=tokenizer)
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
	
	def read_expression(tokenizer, inheritable_give_back_stop_at, vector_mode=False):
		vector_mode_tokens = []
		if vector_mode:
			vector_mode_tokens = [vector_cross_token]
		
		namespace_expression = NamespaceExpression(tokenizer=tokenizer)
		tokenizer.add_expression(namespace_expression, tokenizer.get_symbol(tokenizer.buffer))
		tokenizer.file.give_character_back()
		while (
			tokenizer.file.read_character() == ":"
			and tokenizer.file.read_character() == ":"
			and valid_start_of_symbol.match(tokenizer.file.peek_next_character(ignore_whitespace=False))
		):
			tokenizer.tokenize(stop_ats=[], give_back_stop_ats=inheritable_give_back_stop_at + [semicolon_token, namespace_token, operator_token_without_concatenation, closing_parenthesis_token, closing_bracket_token, chaining_token, template_literal_token, whitespace] + vector_mode_tokens, tree=namespace_expression, read_spaces=True)
		tokenizer.file.give_character_back(ignore_whitespace=True)
			
		return namespace_expression