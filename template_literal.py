from regex import template_literal_token

class TemplateLiteral:
	def __init__(self, value, templates):
		self.value = value
		self.templates = templates
	
	def __str__(self):
		return f"TemplateLiteral({self.value}, {self.templates})"
	
	def to_script(self):
		output = ""
		for index in range(0, len(self.value) - 1):
			output = self.value[index] + f'" @ ({self.templates[index].to_script()}) @ "' + self.value[index + 1]
		return f'"{output}"'