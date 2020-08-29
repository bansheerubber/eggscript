keyword_regexes = {}

class Expression:
	def __init__(self, expressions=None):
		if expressions == None:
			self.expressions = []
		else:
			self.expressions = expressions
		
		self.is_code_block = False
		self.parent = None
		self.is_chainable = False
	
	def handle_semicolon(self):
		if self.parent != None and self.parent.is_code_block and self in self.parent.expressions:
			return ";"
		else:
			return ""
	
	def get_indent_level(self):
		level = 0
		parent = self.parent
		while parent:
			if parent.is_code_block:
				level = level + 1
			parent = parent.parent
		return level
	
	def add_keyword_regex(regex, expression_class):
		keyword_regexes[regex] = expression_class
	
	def read_expression(self):
		print("Unimplemented read_expression()")