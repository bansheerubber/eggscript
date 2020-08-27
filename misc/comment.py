class Comment:
	def __init__(self, comment):
		self.comment = comment
	
	def __str__(self):
		return f"Comment({self.comment})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		return self.comment