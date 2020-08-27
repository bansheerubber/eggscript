class Expression:
	def __init__(self):
		self.expressions = []
	
	def handle_semicolon(self):
		if hasattr(self, "parent") and hasattr(self.parent, "code_block") and self in self.parent.expressions:
			return ";"
		else:
			return ""
	
	def get_indent_level(self):
		level = 0
		parent = self.parent
		while parent:
			level = level + 1
			parent = parent.parent
		return level