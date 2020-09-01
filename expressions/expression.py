keyword_regexes = {}

class Expression:
	def __init__(self, expressions=None, tokenizer=None, no_errors=False, current_line_index=None, current_index=None, current_file_name=None):
		if expressions == None:
			self.expressions = []
		else:
			self.expressions = expressions
		
		self.is_code_block = False
		self.parent = None
		self.is_chainable = False
		self.has_arguments = False
		self.no_keywords_in_code_block = False

		if current_line_index != None and current_index != None and current_file_name != None:
			self.current_line_index = current_line_index
			self.current_index = current_index
			self.current_file_name = current_file_name
		elif tokenizer != None and no_errors == False:
			self.current_line_index = tokenizer.file.current_line_index
			self.current_index = tokenizer.file.current_index
			self.current_file_name = tokenizer.file.filename
		elif no_errors == False:
			raise Exception(f"Expected tokenizer argument for expression {type(self)}")
	
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
	
	def read_expression(tokenizer):
		print("Unimplemented read_expression()")
	
	def safe_get_index(self, index):
		if index < len(self.expressions):
			return self.expressions[index]
		else:
			return None