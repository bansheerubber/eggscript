from argument_expression import ArgumentExpression
from config import get_config
from expression import Expression

class NewObjectExpression(Expression):
	def __init__(self):
		self.class_expressions = None
		self.argument_expressions = []
		self.expressions = []
		self.code_block = True
	
	def convert_expressions_to_class(self):
		self.class_expressions = self.expressions
		self.expressions = []
	
	def convert_expressions_to_arguments(self):
		if len(self.expressions) > 0:
			self.argument_expressions.append(ArgumentExpression(self.expressions))
			self.expressions = []
	
	def __str__(self):
		return f"NewObjectExpression({self.class_expressions}, {self.expressions})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		newline = "\n"
		space = " "
		tab = "\t"
		if get_config("minify") == True:
			newline = ""
			space = ""
			tab = ""

		output = ""
		for class_expression in self.class_expressions:
			output = output + class_expression.to_script()
		
		full_output = "new " + output

		output = ""
		for argument_expression in self.argument_expressions:
			output = output + argument_expression.to_script()

		full_output = full_output + "(" + output + ")" + space + "{" + newline
		
		output = ""
		for expression in self.expressions:
			output = output + (tab * self.get_indent_level()) + expression.to_script() + newline
		
		full_output = full_output + output + (tab * (self.get_indent_level() - 1)) + "}" + self.handle_semicolon()

		return full_output