from eggscript_src.config import get_config
from eggscript_src.expressions.expression import Expression
from eggscript_src.regex import modulus_next_character_token, operator_token, part_of_operator, text_operators, valid_operator

class OperatorExpression(Expression):
	def __init__(self, operator, tokenizer=None, no_errors=False):
		super().__init__(tokenizer=tokenizer, no_errors=no_errors)
		self.operator = operator
		self.parent = None
	
	def __str__(self):
		return f"OperatorExpression({self.operator})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		space = " "
		if get_config("minify") == True and text_operators.match(self.operator) == None:
			space = ""
		
		return f"{space}{self.operator.strip()}{space}"
	
	def read_expression(tokenizer):
		tokenizer.file.give_character_back()
		buffer = ""
		operator_ban_index = 0
		saved_operator = None
		encountered_spaces = 0
		index = 0
		while True:
			char = tokenizer.file.read_character(ignore_whitespace=False)
			if char == " ":
				encountered_spaces = encountered_spaces + 1

			if operator_token.match(char) or part_of_operator.match(char):
				buffer = buffer + char
			else:
				operator_ban_index = index - encountered_spaces
				break
			
			if valid_operator.match(buffer):
				saved_operator = buffer
			
			index = index + 1

		if saved_operator != None:
			difference = len(buffer) - len(saved_operator)
			for i in range(0, difference + 1):
				tokenizer.file.give_character_back()
			
			# special case for namespaces and modulus
			next_char = tokenizer.file.read_character()
			if (
				(next_char == ":" and saved_operator == ":")
				or (modulus_next_character_token.match(next_char) == None and saved_operator == "%")
			):
				tokenizer.file.give_character_back()
				tokenizer.file.give_character_back()
				tokenizer.operator_ban = (tokenizer.file.current_line_index, tokenizer.file.current_index + 1)
				return None
			else:
				tokenizer.file.give_character_back()
			
			return OperatorExpression(saved_operator, tokenizer=tokenizer)
		else:
			for i in range(0, operator_ban_index + encountered_spaces + 1):
				tokenizer.file.give_character_back()
			tokenizer.operator_ban = (tokenizer.file.current_line_index, tokenizer.file.current_index + 1)
			return None

OperatorExpression.operator_precedence = {
	"+": 0,
	"-": 0,
	"*": 1,
	"/": 1,
	".": 1,
	"#": 1,
}