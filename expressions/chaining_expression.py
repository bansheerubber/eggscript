from expression import Expression
from regex import chaining_token, closing_bracket_token, closing_parenthesis_token, operator_token_without_concatenation, semicolon_token

class ChainingExpression(Expression):
	def __init__(self):
		super().__init__()
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
	
	def read_expression(tokenizer, tree, inheritable_give_back_stop_at):
		first_expression = None
		if len(tree.expressions) > 0 and tree.expressions[-1].is_chainable:
			first_expression = tree.expressions.pop()
		else:
			first_expression = tokenizer.get_symbol(tokenizer.buffer)
			tokenizer.buffer = ""
		
		chaining_expression = ChainingExpression()
		tokenizer.add_expression(chaining_expression, first_expression)
		tokenizer.file.give_character_back()
		while tokenizer.file.read_character() == ".":
			tokenizer.tokenize(stop_ats=[], give_back_stop_ats=inheritable_give_back_stop_at + [semicolon_token, chaining_token, operator_token_without_concatenation, closing_parenthesis_token, closing_bracket_token], tree=chaining_expression)
		tokenizer.file.give_character_back()

		return chaining_expression