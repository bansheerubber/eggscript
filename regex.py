import re

colon_token = re.compile(r':')
comment_token = re.compile(r'\/')
chaining_token = re.compile(r'\.')
closing_curly_bracket_token = re.compile(r'}')
closing_bracket_token = re.compile(r'\]')
closing_parenthesis_token = re.compile(r'\)')
comma_token = re.compile(',')
digits = re.compile(r'(-|)\d+\.?\d*')
keywords = re.compile(r'(function|for|while|if|else|else if|switch|switch\$|case|default|package|return|break|continue|datablock|new)$')
namespace_token = re.compile(r':')
opening_curly_bracket_token = re.compile(r'{')
opening_bracket_token = re.compile(r'\[')
opening_parenthesis_token = re.compile(r'\(')
operator_token = re.compile(r'[@&|=\-+*\/^!~><,S@TN?$:]')
operator_token_only_concatenation = re.compile(r'[STN]')
operator_token_without_concatenation = re.compile(r'[@&|=\-+*\/^!~><,@?$:]')
parentheses_token = re.compile(r'[()]')
part_of_operator = re.compile(r'[SPCNLTAB]')
template_literal_token = re.compile(r'{|}')
semicolon_token = re.compile(r';')
space_token = re.compile(r'\s')
string_token = re.compile(r'\"|\'')
valid_assignment = re.compile(r'(=|<<=|>>=|%=|\+=|-=|&=|\|=|\*=|\/=|\^=)$')
valid_break = re.compile(r'break$')
valid_case = re.compile(r'case$')
valid_conditional = re.compile(r'(if|else|else(\w+)if)$')
valid_continue = re.compile(r'continue$')
valid_comment = re.compile(r'\/\/')
valid_datablock = re.compile(r'datablock$')
valid_default = re.compile(r'default$')
valid_for = re.compile(r'for$')
valid_function = re.compile(r'function$')
valid_new = re.compile(r'new$')
valid_operator = re.compile(r'(\+\+|--|&&|\|\||\/\/|<<=|>>=|%=|\+=|-=|&=|\|=|\*=|\/=|\^=|\$=|!\$=|!=|==|=|<=|>=|\*|\/|-|\+|\^|\||&|%|!|<|>|@|SPC|NL|TAB|\?|~|:)$')
valid_package = re.compile(r'package$')
valid_postfix = re.compile(r'(\+\+|--)$')
valid_return = re.compile(r'return$')
valid_symbol = re.compile(r'(%|\$|)([A-Za-z_][A-Za-z0-9_]*)$')
valid_switch = re.compile(r'switch$')
valid_switch_string = re.compile(r'switch\$$')
valid_while = re.compile(r'while$')
variable_token = re.compile(r'%|\$')
whitespace = re.compile(r'[\s\n\r]')