from regex import digits

class Literal:
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return f"Literal({self.value})"
	
	def to_script(self):
		if digits.match(self.value):
			return self.value
		else:
			return f'"{self.value}"'