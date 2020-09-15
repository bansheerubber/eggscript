config = {
	"exportedlines": 0,
	"readfiles": 0,
	"parsedlines": 0,
	"skippedfiles": 0,
}
def get_config(flag):
	if flag not in config:
		return None
	else:
		return config[flag]

def set_config(flag, value):
	config[flag] = value

def add_parsed_lines(count):
	config["parsedlines"] = config["parsedlines"] + count

def add_exported_lines(count):
	config["exportedlines"] = config["exportedlines"] + count

def add_read_file():
	config["readfiles"] = config["readfiles"] + 1

def add_skipped_file():
	config["skippedfiles"] = config["skippedfiles"] + 1