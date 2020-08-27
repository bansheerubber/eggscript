class StringLiteral:
	def __init__(self, value, delimiter):
		self.value = value
		self.delimiter = delimiter
		self.parent = None
	
	def __str__(self):
		return f"StringLiteral({self.delimiter}{self.value}{self.delimiter})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		return f'{self.delimiter}{self.value}{self.delimiter}'