from regex import whitespace

class File:
	def __init__(self, filename):
		self.file = open(filename, "r")
		self.current_line = None
		self.current_index = 0
	
	def read_line(self):
		line = self.file.readline()
		if not line:
			raise Exception("EOF")
		else:
			return line
	
	def read_character(self, ignore_whitespace=True):
		if self.current_line == None or len(self.current_line) <= self.current_index:
			self.current_line = self.read_line()
			self.current_index = 0
		
		char = self.current_line[self.current_index]
		self.current_index = self.current_index + 1
		while whitespace.match(char) and ignore_whitespace:
			char = self.current_line[self.current_index]
			self.current_index = self.current_index + 1

		return char
	
	def give_character_back(self):
		self.current_index = self.current_index - 1