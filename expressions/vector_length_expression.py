from parentheses_expression import ParenthesesExpression
from method_expression import MethodExpression
from symbol import Symbol

class VectorLengthExpression(ParenthesesExpression):
	def __init__(self):
		super().__init__()
		self.parent = None
		self.is_chainable = True
	
	def __str__(self):
		return f"ParenthesesExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):		
		if len(self.expressions) == 0:
			raise Exception("Empty vector length expression")
		
		if (
			len(self.expressions) == 1
			and type(self.expressions[0]) == MethodExpression
			and self.expressions[0].method_symbol.name == "vectorSub"
		):
			# change name of the expression
			self.expressions[0].method_symbol = Symbol("vectorDist")
			return self.expressions[0].to_script()
		else:
			method_expression = MethodExpression(Symbol("vectorLen"))
			method_expression.parent = self.parent

			method_expression.expressions = self.expressions
			method_expression.convert_expressions_to_arguments()

			return method_expression.to_script()