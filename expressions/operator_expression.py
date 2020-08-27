from config import get_config

class OperatorExpression:
	def __init__(self, operator):
		self.operator = operator
		self.parent = None
	
	def __str__(self):
		return f"OperatorExpression({self.operator})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		space = " "
		if get_config("minify") == True:
			space = ""
		
		return f"{space}{self.operator.strip()}{space}"