class Symbol:
	def __init__(self, name):
		self.name = name
	
	def __str__(self):
		return f"Symbol({self.name})"
	
	def to_script(self):
		return self.name