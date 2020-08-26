class ScriptFile:
	def __init__(self, filename):
		self.expressions = []
		self.filename = filename
	
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
			new_line = "\n"
			if hasattr(expression, "no_new_line") == True:
				new_line = ""
			
			output = output + expression.to_script() + new_line
		return output