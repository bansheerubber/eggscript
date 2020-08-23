from file import File
from literal import Literal
from template_literal import TemplateLiteral
from regex import template_literal_token, semicolon, string_token, valid_variable_name, variable_token
from variable import Variable
from variable_assignment import VariableAssignment

def read_variable_name(file):
	# keep reading until we absorb the full variable
	variable_name = file.read_character()
	while valid_variable_name.fullmatch(variable_name) or len(variable_name) == 1:
		char = file.read_character()
		variable_name = variable_name + char
	file.give_character_back()
	return variable_name[0:-1]

def read_variable_assignment(file, stop_ats):
	variable_name = read_variable_name(file)
	
	# absorb equals sign
	char = file.read_character()
	for stop_at in stop_ats:
		if stop_at.match(char):
			print(f"Warning: Shouldn't be finding normal variable '{variable_name}' in variable assignment")
			return Variable(variable_name)

	if char != "=":
		raise Exception(f"Unexpected token '{char}' in variable assignment")
	
	# keep reading until we absorb the full value (ended by semicolon)
	stop_ats.append(semicolon)
	return VariableAssignment(variable_name, tokenize(file, stop_ats=stop_ats, state=0b100))

def read_string(file):
	has_ended = False
	output = ['']
	templates = []
	is_template_literal = False
	while has_ended == False:
		char = file.read_character(ignore_whitespace=False)
		# if we read a backslash, imeditally read the next character so we don't trip up on \" or \'
		if char == "\\":
			output[len(output) - 1] = output[len(output) - 1] + char + file.read_character(ignore_whitespace=False)
			continue
		elif template_literal_token.match(char):
			is_template_literal = True
			templates.append(tokenize(file, stop_ats=[template_literal_token], state=0b11))
			output.append('')
		elif string_token.match(char):
			has_ended = True
		else:
			output[len(output) - 1] = output[len(output) - 1] + char

	if is_template_literal == False:
		return Literal(output[0])
	else:
		return TemplateLiteral(output, templates)

'''
state bitmask

1st: we're in neutral state (waiting for variable assignment, method call, etc)
2st: stop after we have first tree value
3nd: variable assignment
'''
def tokenize(file, stop_ats=[], state=0b1):
	tree = None
	while True:
		if tree != None and state & 0b10:
			return tree
		
		char = ''
		try:
			char = file.read_character()
		except:
			print("Finished file")
			break
			
		for stop_at in stop_ats:
			if stop_at.match(char):
				return tree

		# we're dealing with a variable assignment
		if variable_token.match(char) and state & 0b1:
			file.give_character_back()
			tree = read_variable_assignment(file, stop_ats)
			print(tree.to_script())
		# we're dealing with a string during variable assignment
		elif string_token.match(char) and state & 0b100:
			tree = read_string(file)
	return tree

def tokenize_file(filename):
	file = File(filename)
	tokenize(file)

tokenize_file("test.egg")