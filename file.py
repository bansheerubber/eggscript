from regex import whitespace

class File:
	def __init__(self, filename):
		self.file = open(filename, "r")
		self.current_line = None
		self.current_line_index = 0
		self.line_count = 0
		self.current_index = 0
	
	def read_line(self):
		line = self.file.readline()
		self.line_count = self.line_count + 1
		if not line:
			raise Exception("EOF")
		else:
			return line
	
	# absorbs the rest of the line
	def absorb_line(self):
		rest = self.current_line[self.current_index:-1]
		self.current_line = self.read_line()
		self.current_line_index = self.current_line_index + 1
		self.current_index = 0
		return rest
	
	def read_character(self, ignore_whitespace=True):
		if self.current_line == None or len(self.current_line) <= self.current_index:
			self.current_line = self.read_line()
			self.current_line_index = self.current_line_index + 1
			self.current_index = 0
		
		self.skipped_space = False
		char = self.current_line[self.current_index]
		self.current_index = self.current_index + 1
		while whitespace.match(char) != None and ignore_whitespace and len(self.current_line) > self.current_index:
			char = self.current_line[self.current_index]
			self.current_index = self.current_index + 1
			self.skipped_space = True

		if len(self.current_line) == self.current_index and whitespace.match(char) != None:
			return ''
		else:
			return char
	
	def give_character_back(self):
		self.current_index = self.current_index - 1