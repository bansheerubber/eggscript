from regex import digits

class Literal:
	def __init__(self, value):
		self.value = value
		self.parent = None
	
	def __str__(self):
		return f"Literal({self.value})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		if digits.match(self.value):
			return self.value
		else:
			return f'"{self.value}"'