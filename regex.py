import re

comment_token = re.compile(r'\\/')
chaining_token = re.compile(r'\.')
closing_bracket_token = re.compile(r'}')
closing_parenthesis_token = re.compile(r'\)')
comma_token = re.compile(',')
digits = re.compile(r'(-|)\d+')
keywords = re.compile(r'(function|for|while|if|else|else if)$')
namespace_token = re.compile(r':')
opening_parenthesis_token = re.compile(r'\(')
operator_token = re.compile(r'[@&|=\-+*\/^!~><,S@TN?$]')
operator_token_only_concatenation = re.compile(r'[STN]')
operator_token_without_concatenation = re.compile(r'[@&|=\-+*\/^!~><,@?$]')
parentheses_token = re.compile(r'[()]')
template_literal_token = re.compile(r'{|}')
semicolon_token = re.compile(r';')
string_token = re.compile(r'\"|\'')
valid_assignment = re.compile(r'(=|<<=|>>=|%=|\+=|-=|&=|\|=|\*=|\/=|\^=)$')
valid_conditional = re.compile(r'(if|else|else(\w+)if)$')
valid_comment = re.compile(r'\/\/')
valid_for = re.compile(r'for$')
valid_function = re.compile(r'function$')
valid_operator = re.compile(r'(\+\+|--|&&|\|\||\/\/|<<=|>>=|%=|\+=|-=|&=|\|=|\*=|\/=|\^=|\$=|!\$=|!=|==|=|<=|>=|\*|\/|-|\+|\^|\||&|%|!|<|>|@|SPC|NL|TAB|\?|~)$')
valid_postfix = re.compile(r'(\+\+|--)$')
valid_symbol = re.compile(r'(%|\$|)([A-Za-z_][A-Za-z0-9_]*)$')
valid_while = re.compile(r'while$')
variable_token = re.compile(r'%|\$')
whitespace = re.compile(r'[\s\n\r]')