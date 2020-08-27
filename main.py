from file import File
from tokenizer import Tokenizer
from script_file import ScriptFile

from config import set_config

set_config("minify", True)

def tokenize_file(filename):
	file = File(filename)
	script_file = ScriptFile(filename)
	tokenizer = Tokenizer(file)
	tokenizer.tokenize(tree=script_file)
	script_file.debug()
	print(script_file.to_script())

tokenize_file("test.egg")