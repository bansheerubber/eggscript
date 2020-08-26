class ScriptFile:
	def __init__(self, filename):
		self.expressions = []
		self.filename = filename
		self.parent = None
		self.code_block = True
	
	def __str__(self):
		return f"ScriptFile({self.filename})"
	
	def __repr__(self):
		return self.__str__()
	
	def debug(self):
		for expression in self.expressions:
			print(expression)

	def to_script(self):
		output = ""
		for expression in self.expressions:
			output = output + expression.to_script() + "\n"
		return output