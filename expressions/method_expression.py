from argument_expression import ArgumentExpression
from config import get_config
from expression import Expression
import re
from regex import closing_parenthesis_token, semicolon_token

class MethodExpression(Expression):
	def __init__(self, method_symbol):
		super().__init__()
		self.method_symbol = method_symbol
		self.argument_expressions = []
		self.parent = None
		self.is_chainable = True
		self.has_arguments = True
	
	def convert_expressions_to_arguments(self):
		if len(self.expressions) > 0:
			self.argument_expressions.append(ArgumentExpression(expressions=self.expressions))
			self.expressions = []
	
	def __str__(self):
		return f"MethodExpression({self.metmethod_symbolhod_name}, {self.argument_expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		space = " "
		if get_config("minify") == True:
			space = ""
		
		value = "  "
		for argument in self.argument_expressions:
			value = (value + argument.to_script() + "," + space)

		return f"{self.method_symbol.to_script()}({re.sub(r',$', '', value.strip())}){self.handle_semicolon()}"
	
	def read_expression(tokenizer):
		expression = MethodExpression(tokenizer.get_symbol(tokenizer.buffer))
		tokenizer.buffer = ""
		tokenizer.tokenize(stop_ats=[closing_parenthesis_token], give_back_stop_ats=[semicolon_token], tree=expression)
		expression.convert_expressions_to_arguments()
		return expression