from eggscript_src.regex import digits
from eggscript_src.expressions.expression import Expression

class Literal(Expression):
	def __init__(self, value):
		super().__init__(no_errors=True)
		self.value = value
		self.parent = None
	
	def __str__(self):
		return f"Literal({self.value})"
	
	def __repr__(self):
		return self.__str__()
	
	def is_number(self):
		return isinstance(self.value, int) or digits.match(self.value)
	
	def to_script(self):
		if self.is_number():
			return str(self.value)
		else:
			return f'"{self.value}"'