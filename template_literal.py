from regex import template_literal_token

class TemplateLiteral:
	def __init__(self):
		self.strings = []
		self.expressions = []
		self.templates = []
	
	def __str__(self):
		return f"TemplateLiteral({self.strings}, {self.templates})"
	
	def __repr__(self):
		return self.__str__()
	
	def add_template(self):
		self.templates.append(self.expressions)
		self.expressions = []
	
	def to_script(self):
		output = ""
		for index in range(0, len(self.strings) - 1):
			expression_output = ""
			for expression in self.templates[index]:
				expression_output = expression_output + expression.to_script()
			output = output + self.strings[index] + f'" @ ({expression_output}) @ "'
		
		output = output + self.strings[len(self.strings) - 1]

		return f'"{output}"'