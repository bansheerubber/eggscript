config = {}
def get_config(flag):
	if flag not in config:
		return None
	else:
		return config[flag]

def set_config(flag, value):
	config[flag] = value

def add_parsed_lines(count):
	if "parsedlines" not in config:
		config["parsedlines"] = 0
	
	config["parsedlines"] = config["parsedlines"] + count

def add_exported_lines(count):
	if "exportedlines" not in config:
		config["exportedlines"] = 0
	
	config["exportedlines"] = config["exportedlines"] + count

def add_read_file():
	if "readfiles" not in config:
		config["readfiles"] = 0
	
	config["readfiles"] = config["readfiles"] + 1