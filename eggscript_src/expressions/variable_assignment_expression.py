from eggscript_src.expressions.expression import Expression
from eggscript_src.regex import semicolon_token
from eggscript_src.syntax_exception import SyntaxException

class VariableAssignmentExpression(Expression):
	def __init__(self, assignment_operator, left_hand_expression, tokenizer=None):
		super().__init__(tokenizer=tokenizer)
		self.assignment_operator = assignment_operator
		self.left_hand_expression = left_hand_expression
		self.parent = None
	
	def __str__(self):
		return f"VariableAssignment({self.left_hand_expression}, {self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		value = ""
		for expression in self.expressions:
			value = value + expression.to_script()

		if value == "":
			raise SyntaxException(self, f"Variable assignment syntax error: could not find right hand side value '{self.left_hand_expression}'")

		return f"{self.left_hand_expression.to_script()}{self.assignment_operator.to_script()}{value}{self.handle_semicolon()}" 
	
	def read_expression(tokenizer, operator, left_hand, stop_ats):
		# keep reading until we absorb the full value (ended by semicolon)
		expression = VariableAssignmentExpression(operator, left_hand, tokenizer=tokenizer)
		tokenizer.tokenize(stop_ats=[semicolon_token] + stop_ats, give_back_stop_ats=[semicolon_token] + stop_ats, tree=expression)
		return expression
