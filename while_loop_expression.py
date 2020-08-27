from expression import Expression

class WhileLoopExpression(Expression):
	def __init__(self):
		self.expressions = []
		self.conditional_expressions = []
		self.code_block = True
	
	def convert_expressions_to_conditionals(self):
		self.conditional_expressions = self.expressions
		self.expressions = []
	
	def __str__(self):
		return f"WhileLoopExpression({self.conditional_expressions}, {self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		full_output = ""

		output = ""
		for conditional_expression in self.conditional_expressions:
			output = output + conditional_expression.to_script()

		full_output = "while(" + output + ") {\n"
		
		output = ""
		for expression in self.expressions:
			output = output + ("\t" * self.get_indent_level()) + expression.to_script() + "\n"
		
		full_output = full_output + output[0:-1] + "\n" + ("\t" * (self.get_indent_level() - 1)) + "}"

		return full_output