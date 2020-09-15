from parentheses_expression import ParenthesesExpression
from method_expression import MethodExpression
from symbol import Symbol
from syntax_exception import SyntaxException
from regex import vector_length_token

class VectorLengthExpression(ParenthesesExpression):
	def __init__(self, tokenizer=None):
		super().__init__(tokenizer=tokenizer)
		self.parent = None
		self.is_chainable = True
	
	def __str__(self):
		return f"ParenthesesExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):		
		if len(self.expressions) == 0:
			raise SyntaxException(self, "Vector length exception: empty expression")
		
		if (
			len(self.expressions) == 1
			and type(self.expressions[0]) == MethodExpression
			and self.expressions[0].method_symbol.name == "vectorSub"
		):
			# change name of the expression
			self.expressions[0].method_symbol = Symbol("vectorDist")
			return self.expressions[0].to_script()
		else:
			method_expression = MethodExpression(Symbol("vectorLen"), current_line_index=self.current_line_index, current_index=self.current_index, current_file_name=self.current_file_name)
			method_expression.parent = self.parent

			method_expression.expressions = self.expressions
			method_expression.convert_expressions_to_arguments()

			return method_expression.to_script()
	
	def read_expression(tokenizer):
		if vector_length_token.match(tokenizer.file.read_character()) == None:
			raise SyntaxException(self, "Vector length expression syntax error: no double |'s found")
		
		expression = VectorLengthExpression(tokenizer=tokenizer)
		tokenizer.tokenize(stop_ats=[vector_length_token], tree=expression)

		if vector_length_token.match(tokenizer.file.read_character()) == None:
			raise SyntaxException(self, "Vector length expression syntax error: no double |'s found")

		return expression
