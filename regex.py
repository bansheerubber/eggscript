import re

assignment_token = re.compile('=')
chaining_token = re.compile('\.')
digits = re.compile('(-|)\d+')
operator_token = re.compile('[()@&|=\\-+*\\/^!~><]')
template_literal_token = re.compile('{|}')
semicolon = re.compile(';')
string_token = re.compile('\"|\'')
valid_symbol = re.compile('(%|\$|)([A-Za-z_][A-Za-z0-9_]*)$')
variable_token = re.compile('%|\\$')
whitespace = re.compile('[\s\n\r]')