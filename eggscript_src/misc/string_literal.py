from eggscript_src.expressions.expression import Expression
from eggscript_src.expressions.template_literal_expression import TemplateLiteralExpression
from eggscript_src.regex import template_literal_token

class StringLiteral(Expression):
	def __init__(self, value, delimiter, tokenizer=None):
		super().__init__(tokenizer=tokenizer)
		self.value = value
		self.delimiter = delimiter
		self.parent = None
	
	def __str__(self):
		return f"StringLiteral({self.delimiter}{self.value}{self.delimiter})"
	
	def __repr__(self):
		return self.__str__()
	
	def to_script(self):
		return f'{self.delimiter}{self.value}{self.delimiter}'
	
	def read_expression(tokenizer, is_template=False):
		tokenizer.file.give_character_back()
		delimiter = tokenizer.file.read_character()
		
		has_ended = False
		output = [''] # list of values with templates inbetween them
		template_literal = None
		while has_ended == False:
			char = tokenizer.file.read_character(ignore_whitespace=False)
			# if we read a backslash, imeditally read the next character so we don't trip up on \" or \'
			if char == "\\":
				output[len(output) - 1] = output[len(output) - 1] + char + tokenizer.file.read_character(ignore_whitespace=False)
				continue
			elif is_template == True and template_literal_token.match(char):
				if template_literal == None:
					template_literal = TemplateLiteralExpression(tokenizer=tokenizer) # create template literal if we don't have one
				# tokenize b/c we're parsing runnable code
				tokenizer.tokenize(stop_ats=[template_literal_token], tree=template_literal)
				# move the templates over to a new list
				template_literal.add_template()
				# add a new value
				output.append('')
			elif char == delimiter: # find the last " or '
				has_ended = True
			else: # add to the value
				output[len(output) - 1] = output[len(output) - 1] + char

		if template_literal == None:
			return StringLiteral(output[0], delimiter, tokenizer=tokenizer)
		else:
			template_literal.strings = output
			return template_literal