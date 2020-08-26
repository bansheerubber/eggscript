class Expression:
	def __init__(self):
		self.expressions = []
	
	def handle_semicolon(self):
		if hasattr(self, "parent") and hasattr(self.parent, "code_block") and self in self.parent.expressions:
			return ";"
		else:
			return ""