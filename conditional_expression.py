from expression import Expression

class ConditionalExpression(Expression):
	def __init__(self):
		self.conditional_expressions = []
		self.expressions = []
		self.code_block = True
		self.type = ""
	
	def __str__(self):
		return f"ConditionalExpression({self.type}, {self.conditional_expressions}, {self.expressions})"
	
	def __repr__(self):
		return self.__str__()

	def move_expressions(self):
		self.conditional_expressions = self.expressions
		self.expressions = []
	
	def to_script(self):
		full_output = ""
		
		if self.type != "else":
			output = ""
			for conditional_expression in self.conditional_expressions:
				output = output + conditional_expression.to_script()
			
			full_output = self.type + "(" + output + ") {\n"
		else:
			full_output = self.type + " {\n"
		
		output = ""
		for expression in self.expressions:
			output = output + ("\t" * self.get_indent_level()) + expression.to_script() + "\n"
		
		full_output = full_output + output[0:-1] + "\n" + ("\t" * (self.get_indent_level() - 1)) + "}"

		return full_output