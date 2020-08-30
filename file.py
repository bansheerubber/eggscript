from config import add_parsed_lines
from regex import whitespace

class File:
	def __init__(self, filename):
		self.file = open(filename, "r")
		self.current_line = None
		self.current_line_index = -1
		self.current_index = 0
		self.lines = []
		self.eat_file()
	
	def eat_file(self):
		for line in self.file:
			self.lines.append(line)
		add_parsed_lines(len(self.lines))
	
	# absorbs the rest of the line
	def absorb_line(self):
		rest = self.current_line[self.current_index:-1]
		self.current_line_index = self.current_line_index + 1
		if self.current_line_index < len(self.lines):
			self.current_line = self.lines[self.current_line_index]			

		self.current_index = 0
		return rest
	
	def read_character(self, ignore_whitespace=True):
		if self.current_line_index >= len(self.lines):
			raise Exception("EOF")
		
		if self.current_line == None or len(self.current_line) <= self.current_index:
			self.current_line_index = self.current_line_index + 1

			if self.current_line_index >= len(self.lines):
				raise Exception("EOF")

			self.current_line = self.lines[self.current_line_index]
			self.current_index = 0
		
		self.skipped_space = False
		char = self.current_line[self.current_index]
		self.current_index = self.current_index + 1
		while whitespace.match(char) != None and ignore_whitespace:
			if len(self.current_line) > self.current_index:
				char = self.current_line[self.current_index]
				self.current_index = self.current_index + 1
				self.skipped_space = True
			else:
				self.current_line_index = self.current_line_index + 1

				if self.current_line_index >= len(self.lines):
					raise Exception("EOF")
				
				self.current_line = self.lines[self.current_line_index]
				self.current_index = 0

		if len(self.current_line) == self.current_index and whitespace.match(char) != None:
			return ''
		else:
			return char
	
	def give_character_back(self, ignore_whitespace=False):
		self.current_index = self.current_index - 1
		if self.current_index < 0:
			self.current_line_index = self.current_line_index - 1 # step back one line
			self.current_line = self.lines[self.current_line_index]
			self.current_index = len(self.current_line) - 1
		char = self.current_line[self.current_index]

		while whitespace.match(char) != None and ignore_whitespace:
			self.current_index = self.current_index - 1
			if self.current_index < 0:
				self.current_line_index = self.current_line_index - 1 # step back one line
				self.current_line = self.lines[self.current_line_index]
				self.current_index = len(self.current_line) - 1
			char = self.current_line[self.current_index]

		return self.current_line[self.current_index]