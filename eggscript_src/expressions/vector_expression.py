from eggscript_src.expressions.chaining_expression import ChainingExpression
from enum import IntEnum
from eggscript_src.expressions.expression import Expression
from eggscript_src.misc.literal import Literal
from eggscript_src.expressions.method_expression import MethodExpression
from eggscript_src.expressions.operator_expression import OperatorExpression
from eggscript_src.expressions.parentheses_expression import ParenthesesExpression
from eggscript_src.regex import closing_parenthesis_token, closing_vector_escape_token, opening_parenthesis_token, opening_vector_escape_token, vector_cross_token, vector_escape_token, vector_length_token, vector_operator_tokens, vector_together_components, vector_token, vector_valid_replacements
from eggscript_src.misc.symbol import Symbol
from eggscript_src.syntax_exception import SyntaxException
from eggscript_src.expressions.vector_escape_expression import VectorEscapeExpression
from eggscript_src.expressions.vector_length_expression import VectorLengthExpression
from eggscript_src.warn import warn

class VectorExpression(Expression):
	def __init__(self, tokenizer=None):
		super().__init__(tokenizer=tokenizer)
		self.parent = None
	
	def __str__(self):
		return f"VectorExpression({self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		self.convert_expression()
		
		output = ""
		for expression in self.expressions:
			output = output + expression.to_script()
		
		return f'{output}{self.handle_semicolon()}'
	
	def read_expression(tokenizer, expression=None):
		if expression == None:
			expression = VectorExpression(tokenizer=tokenizer)

		stop_ats = [closing_parenthesis_token, opening_parenthesis_token, vector_escape_token, vector_length_token, vector_operator_tokens, vector_token]
		if type(expression) == VectorEscapeExpression:
			stop_ats = [vector_escape_token]

		tokenizer.tokenize(stop_ats=[vector_token], inheritable_give_back_stop_at=[vector_token, vector_cross_token], tree=expression, vector_mode=True) # only support vector operators
		return expression
	
	def convert_expression(self, expression=None):
		self.handle_parentheses_expressions(expression=expression)
		self.handle_method_expressions(expression=expression)
		self.handle_chain_replacements(expression=expression)
		self.handle_order_of_operations(expression=expression)

	def handle_parentheses_expressions(self, expression=None):
		if expression == None:
			expression = self
		
		for found_expression in expression.expressions:
			if type(found_expression) == ParenthesesExpression or type(found_expression) == VectorLengthExpression:
				self.convert_expression(expression=found_expression)
	
	def handle_method_expressions(self, expression=None):
		if expression == None:
			expression = self
		
		for found_expression in expression.expressions:
			if type(found_expression) == MethodExpression:
				for argument_expression in found_expression.argument_expressions:
					self.convert_expression(expression=found_expression)

	# replace x, y, z, or w with getWord substitutes
	def handle_chain_replacements(self, expression=None):
		if expression == None:
			expression = self
		
		def create_method(chain, buffer):
			if buffer == "xyz":
				return chain
			elif buffer == "_":
				return Literal("0")
			elif buffer in VectorExpression.component_table:
				method_data = VectorExpression.component_table[buffer]
				replacement_expression = MethodExpression(method_data[0], tokenizer=expression.tokenizer)
				for index in range(1, len(method_data)):
					element = method_data[index]
					if element == None:
						replacement_expression.expressions.append(chain)
					else:
						replacement_expression.expressions.append(Literal(element))
					replacement_expression.convert_expressions_to_arguments()
				return replacement_expression
			else:
				raise SyntaxException(self, f"Component access '{buffer}' not in component table")
		
		for index in range(0, len(expression.expressions)):
			found_expression = expression.expressions[index]
			if type(found_expression) == ChainingExpression:
				if type(found_expression.tail()) != Symbol:
					continue
				
				tail = found_expression.tail().name
				if vector_valid_replacements.match(tail):
					parentheses_expression = ParenthesesExpression(tokenizer=expression.tokenizer)
					
					buffer = ""
					together_index = 0
					chain = found_expression.splice(0, len(found_expression.expressions) - 1)
					while together_index < len(tail):
						before_match = vector_together_components.match(buffer)
						
						buffer = buffer + tail[together_index]

						if len(buffer) >= 2:
							if vector_together_components.match(buffer) == None:
								replacement_expression = create_method(chain, buffer[0:-1])
								if len(parentheses_expression.expressions) == 0:
									parentheses_expression.expressions.append(replacement_expression)
								else:
									parentheses_expression.expressions.append(OperatorExpression("SPC", tokenizer=expression.tokenizer))
									parentheses_expression.expressions.append(replacement_expression)

								buffer = buffer[-1]
						
						together_index = together_index + 1
					
					replacement_expression = create_method(chain, buffer)
					if len(parentheses_expression.expressions) == 0:
						parentheses_expression.expressions.append(replacement_expression)
					else:
						parentheses_expression.expressions.append(OperatorExpression("SPC", tokenizer=expression.tokenizer))
						parentheses_expression.expressions.append(replacement_expression)

					expression.expressions[index] = parentheses_expression
						
	def handle_order_of_operations(self, offset=0, min_precedence=0, expression=None):
		def is_maybe_scalar_expression(expression):
			# checking to see if this expression is a scalar expression
			if (
				type(expression) == VectorEscapeExpression
				or (
					type(expression) == MethodExpression
					and expression.method_symbol.name == "vectorDot"
					and expression.method_symbol.name == "vectorLen"
				)
				or (
					type(expression) == Literal
					and expression.is_number()
				)
			):
				return True
			else:
				return False
		
		if expression == None:
			expression = self
		
		# fetch operand
		left_vector = expression.safe_get_index(0 + offset)
		if hasattr(left_vector, "operator"): # handling special cases where operators are used to modify a vector (-, ^)
			self.replace_modifier_operation_with_call(offset, expression.safe_get_index(1 + offset), left_vector, expression=expression)
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
		elif (
			left_vector == None
			or (left_vector != None and operator != None and right_vector == None)
		):
			raise SyntaxException(self, "Vector expression syntax error: couldn't find operands")
		elif operator != None and operator.operator not in VectorExpression.operator_table:
			raise SyntaxException(self, f"Vector expression syntax error: invalid operator {operator.operator}")
		elif next_operator != None and next_operator.operator not in VectorExpression.operator_table:
			raise SyntaxException(self, f"Vector expression syntax error: invalid operator {next_operator.operator}")
		
		# check for type errors
		if (
			VectorExpression.operator_allows_scalars[operator.operator] == OperatorScalarOption.NO_SCALARS
		):
			if (
				(
					is_maybe_scalar_expression(left_vector) == True
					and is_maybe_scalar_expression(right_vector) == False
				)
				or (
					is_maybe_scalar_expression(left_vector) == False
					and is_maybe_scalar_expression(right_vector) == True
				)
			):
				raise SyntaxException(self, f"Vector expression syntax error: cannot mix scalars and vectors for operator {operator.operator} at {left_vector.to_script()} {operator.operator} {right_vector.to_script()}")
			elif (
				is_maybe_scalar_expression(left_vector) == True
				and is_maybe_scalar_expression(right_vector) == True
			):
				raise SyntaxException(self, f"Vector expression syntax error: only vector operations are allowed inside backticks, not {left_vector.to_script()} {operator.operator} {right_vector.to_script()}. To escape, use the vector escape syntax " + "{}")
		elif (
			VectorExpression.operator_allows_scalars[operator.operator] == OperatorScalarOption.RIGHT_OR_LEFT_SCALAR
			or VectorExpression.operator_allows_scalars[operator.operator] == OperatorScalarOption.ONLY_RIGHT_SCALAR
		):
			if VectorExpression.operator_allows_scalars[operator.operator] == OperatorScalarOption.ONLY_RIGHT_SCALAR and is_maybe_scalar_expression(left_vector) == True:
				raise SyntaxException(self, f"Vector expression syntax error: the {operator.operator} operator does not support left-handed scalar operations at {left_vector.to_script()} {operator.operator} {right_vector.to_script()}")
			elif (
				is_maybe_scalar_expression(left_vector) == False
				and is_maybe_scalar_expression(right_vector) == False
			):
				warn(self, f"Vector expression syntax warning: implicit usage of scalars for operator {operator.operator} at {left_vector.to_script()} {operator.operator} {right_vector.to_script()}. Will only work at run-time if right-hand side is a scalar")
			elif (
				is_maybe_scalar_expression(left_vector) == True
				and is_maybe_scalar_expression(right_vector) == True
			):
				raise SyntaxException(self, f"Vector expression syntax error: only vector operations are allowed inside backticks, not {left_vector.to_script()} {operator.operator} {right_vector.to_script()}. To escape, use the vector escape syntax " + "{}")
		# done with syntax errors

		# do precedence rules
		if next_operator != None:
			if OperatorExpression.operator_precedence[operator.operator] >= min_precedence and OperatorExpression.operator_precedence[operator.operator] < OperatorExpression.operator_precedence[next_operator.operator]:
				self.handle_order_of_operations(offset=offset + 2, min_precedence=OperatorExpression.operator_precedence[next_operator.operator], expression=expression)
		
		# these operands may have changed due to precedence rules. re-fetch
		left_vector = expression.safe_get_index(0 + offset)
		right_vector = expression.safe_get_index(2 + offset)

		# determine which vector is a scalar and if we need to flip the sides
		if (
			VectorExpression.operator_allows_scalars[operator.operator] == 1
			and is_maybe_scalar_expression(left_vector)
		):
			right_vector = expression.safe_get_index(0 + offset)
			left_vector = expression.safe_get_index(2 + offset)

		self.replace_operation_with_call(offset, left_vector, operator, right_vector, expression=expression)
		self.handle_order_of_operations(offset=offset, expression=expression)
	
	def replace_modifier_operation_with_call(self, index_of_left, left_vector, operator, expression=None):
		if expression == None:
			expression = self
		
		del expression.expressions[index_of_left:index_of_left + 1]

		if operator.operator not in VectorExpression.modifier_operator_table:
			raise SyntaxException(self, f"Vector syntax error: {operator.operator} is invalid modifier operator")

		modifier_method = VectorExpression.modifier_operator_table[operator.operator]

		expression.expressions[index_of_left] = MethodExpression(modifier_method[0], current_line_index=self.current_line_index, current_index=self.current_index, current_file_name=self.current_file_name)
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

		method = VectorExpression.operator_table[operator.operator]

		expression.expressions[index_of_left] = MethodExpression(method[0], current_line_index=self.current_line_index, current_index=self.current_index, current_file_name=self.current_file_name)
		method_expression = expression.expressions[index_of_left]
		method_expression.parent = expression

		left_vector.parent = method_expression
		right_vector.parent = method_expression

		for argument in method[1]:
			if argument == None:
				method_expression.expressions.append(left_vector)
			else:
				method_expression.expressions.append(argument)
		method_expression.convert_expressions_to_arguments()

		for argument in method[2]:
			if argument == None:
				method_expression.expressions.append(right_vector)
			else:
				method_expression.expressions.append(argument)
		method_expression.convert_expressions_to_arguments()
		method_expression.convert_expressions_to_arguments()

class OperatorScalarOption(IntEnum):
	NO_SCALARS = 0
	RIGHT_OR_LEFT_SCALAR = 1
	ONLY_RIGHT_SCALAR = 2


VectorExpression.operator_allows_scalars = {
	"+": OperatorScalarOption.NO_SCALARS,
	"*": OperatorScalarOption.RIGHT_OR_LEFT_SCALAR,
	"-": OperatorScalarOption.NO_SCALARS,
	"/": OperatorScalarOption.ONLY_RIGHT_SCALAR,
	".": OperatorScalarOption.NO_SCALARS,
	"#": OperatorScalarOption.NO_SCALARS,
}

VectorExpression.operator_table = {
	"+": (Symbol("vectorAdd"), [None], [None]),
	"*": (Symbol("vectorScale"), [None], [None]),
	"-": (Symbol("vectorSub"), [None], [None]),
	"/": (Symbol("vectorScale"), [None], [Literal("1"), OperatorExpression("/", no_errors=True), None]),
	".": (Symbol("vectorDot"), [None], [None]),
	"#": (Symbol("vectorCross"), [None], [None]),
}

VectorExpression.component_table = {
	"x": 		(Symbol("getWord"), None, 0),
	"y": 		(Symbol("getWord"), None, 1),
	"z": 		(Symbol("getWord"), None, 2),
	"w": 		(Symbol("getWord"), None, 3),
	"xy": 	(Symbol("getWords"), None, 0, 1),
	"xyzw": (Symbol("getWords"), None, 0, 3),
	"yz":		(Symbol("getWords"), None, 1, 2),
	"yzw": 	(Symbol("getWords"), None, 1, 3),
	"zw": 	(Symbol("getWords"), None, 2, 3),
}

VectorExpression.modifier_operator_table = {
	"-": (Symbol("vectorScale"), None, "-1"),
	"^": (Symbol("vectorNormalize"), None),
}