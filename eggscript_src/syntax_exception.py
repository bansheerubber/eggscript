class SyntaxException(Exception):
	def __init__(self, expression, message):
		super().__init__(f"\033[91m{message} at line #{expression.current_line_index} character #{expression.current_index} file '{expression.current_file_name}'\033[0m")