from expression import Expression
from regex import chaining_token, closing_bracket_token, closing_parenthesis_token, operator_token_without_concatenation, semicolon_token, template_literal_token, valid_symbol

class ChainingExpression(Expression):
	def __init__(self, tokenizer=None):
		super().__init__(tokenizer=tokenizer)
		self.parent = None
	
	def __str__(self):
		return f"ChainingExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		output = ""
		for expression in self.expressions:
			output = output + expression.to_script() + "."

		return output[0:-1] + self.handle_semicolon()
	
	def tail(self):
		return self.expressions[-1]
	
	def splice(self, start, stop):
		new_expression = ChainingExpression(tokenizer=self.tokenizer)
		for index in range(start, stop):
			new_expression.expressions.append(self.expressions[index])
		return new_expression
	
	def read_expression(tokenizer, tree, inheritable_give_back_stop_at):
		first_expression = None
		if len(tree.expressions) > 0 and tree.expressions[-1].is_chainable:
			first_expression = tree.expressions.pop()
		else:
			first_expression = tokenizer.get_symbol(tokenizer.buffer)
			tokenizer.buffer = ""
		
		chaining_expression = ChainingExpression(tokenizer=tokenizer)
		tokenizer.add_expression(chaining_expression, first_expression)
		tokenizer.file.give_character_back()
		while tokenizer.file.read_character() == "." and valid_symbol.match(tokenizer.file.peek_next_character()):
			tokenizer.tokenize(stop_ats=[], give_back_stop_ats=inheritable_give_back_stop_at + [semicolon_token, chaining_token, operator_token_without_concatenation, closing_parenthesis_token, closing_bracket_token, template_literal_token], tree=chaining_expression)
		tokenizer.file.give_character_back(ignore_whitespace=True)

		return chaining_expression