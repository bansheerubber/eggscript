class TokenizerException(Exception):
	def __init__(self, tokenizer, message):
		super().__init__(f"{message} at line #{tokenizer.file.line_count} character #{tokenizer.file.current_index}")