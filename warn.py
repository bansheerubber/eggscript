from config import get_config

def warn(expression, message):
	if get_config("no-warnings") != True:
		print(f"\033[93m{message} at line #{expression.current_line_index} character #{expression.current_index} file '{expression.current_file_name}'\033[0m")