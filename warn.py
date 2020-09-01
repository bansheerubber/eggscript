def warn(expression, message):
	print(f"\033[93m{message} at line #{expression.current_line_index} character #{expression.current_index} file '{expression.current_file_name}'\033[0m")