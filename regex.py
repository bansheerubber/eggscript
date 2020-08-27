import re

comment_token = re.compile('\\/')
chaining_token = re.compile('\.')
closing_bracket_token = re.compile('}')
closing_parenthesis_token = re.compile('\\)')
comma_token = re.compile(',')
digits = re.compile('(-|)\d+')
opening_parenthesis_token = re.compile('\\(')
operator_token = re.compile('[@&|=\\-+*\\/^!~><,S@TN?:$]')
parentheses_token = re.compile('[()]')
template_literal_token = re.compile('{|}')
semicolon_token = re.compile(';')
string_token = re.compile('\"|\'')
valid_assignment = re.compile('(=|<<=|>>=|%=|\\+=|-=|&=|\\|=|\\*=|\\/=|\\^=)$')
valid_conditional = re.compile('(if|else|else(\w+)if)')
valid_comment = re.compile('\\/\\/')
valid_operator = re.compile('(\\+\\+|--|&&|\\|\\||\\/\\/|<<=|>>=|%=|\\+=|-=|&=|\\|=|\\*=|\\/=|\\^=|\\$=|!\\$=|!=|==|=|<=|>=|\\*|\\/|-|\\+|\\^|\\||&|%|!|<|>|@|SPC|NL|TAB|\\?|:|~)$')
valid_postfix = re.compile('(\\+\\+|--)$')
valid_symbol = re.compile('(%|\\$|)([A-Za-z_][A-Za-z0-9_]*)$')
variable_token = re.compile('%|\\$')
whitespace = re.compile('[\s\n\r]')