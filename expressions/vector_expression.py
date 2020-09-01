from expression import Expression
from literal import Literal
from method_expression import MethodExpression
from operator_expression import OperatorExpression
from parentheses_expression import ParenthesesExpression
from regex import vector_escape_token, vector_operator_tokens, vector_token
from symbol import Symbol
from vector_escape_expression import VectorEscapeExpression

class VectorExpression(Expression):
	def __init__(self):
		super().__init__()
		self.parent = None
	
	def __str__(self):
		return f"VectorExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		self.handle_parentheses_expressions()
		self.handle_order_of_operations()
		
		output = ""
		for expression in self.expressions:
			output = output + expression.to_script()
		
		return f'{output}{self.handle_semicolon()}'
	
	def read_expression(tokenizer):
		expression = VectorExpression()

		tokenizer.tokenize(give_back_stop_ats=[vector_operator_tokens, vector_token], tree=expression) # only support vector operators
		while vector_token.match(tokenizer.file.read_character()) == None:
			math_operator = OperatorExpression(tokenizer.file.give_character_back())
			tokenizer.file.read_character()

			expression.expressions.append(math_operator)
			math_operator.parent = expression

			tokenizer.tokenize(give_back_stop_ats=[vector_operator_tokens, vector_token], tree=expression)

		return expression
	
	def handle_parentheses_expressions(self, expression=None):
		if expression == None:
			expression = self
		
		for found_expression in expression.expressions:
			if type(found_expression) == ParenthesesExpression:
				self.handle_parentheses_expressions(expression=found_expression)
				self.handle_order_of_operations(expression=found_expression)

	def handle_order_of_operations(self, offset=0, min_precedence=0, expression=None):
		if expression == None:
			expression = self
		
		# fetch operand
		left_vector = expression.safe_get_index(0 + offset)
		if hasattr(left_vector, "operator"): # handling special cases where operators are used to modify a vector (-, ^)
			self.replace_modifier_operation_with_call(offset, self.safe_get_index(1 + offset), left_vector, expression=expression)
			left_vector = expression.safe_get_index(0 + offset)

		# fetch operator
		operator = expression.safe_get_index(1 + offset)

		# fetch operand
		right_vector = expression.safe_get_index(2 + offset)
		if hasattr(right_vector, "operator"): # handling special cases where operators are used to modify a vector (-, ^)
			self.replace_modifier_operation_with_call(2 + offset, expression.safe_get_index(3 + offset), right_vector)
			right_vector = expression.safe_get_index(2 + offset)

		# fetch operator
		next_operator = expression.safe_get_index(3 + offset)

		# if we hit an operator that isn't anything, then we've probably reached the end of our expression. quit
		if operator == None:
			return
		
		# do precedence rules
		if next_operator != None:
			if OperatorExpression.operator_precedence[operator.operator] >= min_precedence and OperatorExpression.operator_precedence[operator.operator] < OperatorExpression.operator_precedence[next_operator.operator]:
				self.handle_order_of_operations(offset=offset + 2, min_precedence=OperatorExpression.operator_precedence[next_operator.operator], expression=expression)
		
		# these operands may have changed due to precedence rules. re-fetch
		left_vector = expression.safe_get_index(0 + offset)
		right_vector = expression.safe_get_index(2 + offset)
		self.replace_operation_with_call(offset, left_vector, operator, right_vector, expression=expression)
		self.handle_order_of_operations(offset=offset)
	
	def replace_modifier_operation_with_call(self, index_of_left, left_vector, operator, expression=None):
		if expression == None:
			expression = self
		
		del expression.expressions[index_of_left:index_of_left + 1]

		modifier_method = VectorExpression.modifier_operator_table[operator.operator]

		expression.expressions[index_of_left] = MethodExpression(modifier_method[0])
		expression.expressions[index_of_left].parent = expression

		for index in range(1, len(modifier_method)):
			if modifier_method[index] == None:
				expression.expressions[index_of_left].expressions.append(left_vector)
				expression.expressions[index_of_left].convert_expressions_to_arguments()
				left_vector.parent = expression.expressions[index_of_left]
			else:
				expression.expressions[index_of_left].expressions.append(Literal(modifier_method[index]))
				expression.expressions[index_of_left].convert_expressions_to_arguments()
	
	def replace_operation_with_call(self, index_of_left, left_vector, operator, right_vector, expression=None):
		if expression == None:
			expression = self
		
		del expression.expressions[index_of_left:index_of_left + 2]

		expression.expressions[index_of_left] = MethodExpression(VectorExpression.operator_table[operator.operator])
		expression.expressions[index_of_left].parent = expression

		left_vector.parent = expression.expressions[index_of_left]
		right_vector.parent = expression.expressions[index_of_left]

		expression.expressions[index_of_left].expressions.append(left_vector)
		expression.expressions[index_of_left].convert_expressions_to_arguments()

		expression.expressions[index_of_left].expressions.append(right_vector)
		expression.expressions[index_of_left].convert_expressions_to_arguments()
	
VectorExpression.operator_table = {
	"+": Symbol("vectorAdd"),
	"*": Symbol("vectorScale"),
	"-": Symbol("vectorSub"),
	"/": Symbol("vectorDivide"),
	".": Symbol("vectorDot"),
}

VectorExpression.modifier_operator_table = {
	"-": (Symbol("vectorScale"), None, "-1"),
	"^": (Symbol("vectorNormalize"), None),
}