from config import get_config
from regex import template_literal_token

class TemplateLiteralExpression:
	def __init__(self):
		self.strings = []
		self.expressions = []
		self.templates = []
		self.parent = None
	
	def __str__(self):
		return f"TemplateLiteralExpression({self.strings}, {self.templates})"
	
	def __repr__(self):
		return self.__str__()
	
	def add_template(self):
		self.templates.append(self.expressions)
		self.expressions = []
	
	def to_script(self):
		space = " "
		if get_config("minify") == True:
			space = ""
		
		output = ""
		for index in range(0, len(self.strings) - 1):
			expression_output = ""
			for expression in self.templates[index]:
				expression_output = expression_output + expression.to_script()
			output = output + self.strings[index] + f'"{space}@{space}({expression_output}){space}@{space}"'
		
		output = output + self.strings[len(self.strings) - 1]

		return f'"{output}"'