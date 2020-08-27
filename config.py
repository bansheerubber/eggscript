config = {}
def get_config(flag):
	if flag not in config:
		return None
	else:
		return config[flag]

def set_config(flag, value):
	config[flag] = value