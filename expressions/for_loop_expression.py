from config import get_config
from expression import Expression

class ForLoopExpression(Expression):
	def __init__(self):
		self.expressions = []
		self.initiation_expressions = []
		self.conditional_expressions = []
		self.increment_expressions = []
		self.code_block = True
	
	def __str__(self):
		return f"ForLoopExpression({self.initiation_expressions}, {self.conditional_expressions}, {self.increment_expressions}, {self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def move_initiation_expressions(self):
		self.initiation_expressions = self.expressions
		self.expressions = []
	
	def move_conditional_expressions(self):
		self.conditional_expressions = self.expressions
		self.expressions = []

	def move_increment_expressions(self):
		self.increment_expressions = self.expressions
		self.expressions = []
	
	def to_script(self):
		full_output = ""

		newline = "\n"
		space = " "
		tab = "\t"
		if get_config("minify") == True:
			newline = ""
			space = ""
			tab = ""
		
		initiation_output = ""
		for initiation_expression in self.initiation_expressions:
			initiation_output = initiation_output + initiation_expression.to_script()
		
		conditional_output = ""
		for conditional_expression in self.conditional_expressions:
			conditional_output = conditional_output + conditional_expression.to_script()
		
		increment_output = ""
		for increment_expression in self.increment_expressions:
			increment_output = increment_output + increment_expression.to_script()
		
		full_output = f"for({initiation_output};{space}{conditional_output};{space}{increment_output})"
		full_output = full_output + space + "{" + newline
		
		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output + (tab * (self.get_indent_level() - 1)) + "}"

		return full_output