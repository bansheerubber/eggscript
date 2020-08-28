from config import get_config
from expression import Expression

class InheritanceExpression(Expression):
	def __init__(self):
		super().__init__()
		self.child_class = None
		self.super_class = None
	
	def convert_expression_to_super_class(self):
		self.super_class = self.expressions[0]
		self.expressions = []
	
	def __str__(self):
		return f"InheritanceExpression({self.child_class}, {self.super_class})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		space = " "
		if get_config("minify") == True:
			space = ""
		
		return f"{self.child_class.to_script()}{space}:{space}{self.super_class.to_script()}"