from config import set_config
from file import File
from tokenizer import Tokenizer
from script_file import ScriptFile

import sys, getopt

def print_help():
	help_list = ["Syntax:   eggscript [files or directory] [options]",
		"Examples: eggscript server.egg",
	  "	  eggscript server.egg -o server.cs",
	  "	  eggscript server.egg -o ./Server_Minigame",
	  "	  eggscript ./Server_Minigame-dev -o ../Server_Minigame -m --no-warnings",
		"",
		"Options:",
		"-h, --help								Show help message",
		"-o [file or directory], --output [file or directory]			Output transpiled TorqueScript file(s) to the specified file or directory. Filenames are preserved by default (server.egg turns into server.cs, example.egg turns into server.cs) if output is a directory.",
		"-f [expression], --file-replace [expression]				Renames output files. Example: -f \"{}.1.cs\" will export all files withe the \".1.cs\" extension. -f \"new_{}.cs\" will export all files with \"new_\" prepended infront of the file name. Default file replace is \"{}.cs\".",
		"-m, --minify								Minify the output files (pretty prints by default)",
		"--no-comments								Do not output comments",
		"--no-warnings								Do not print warnings",
		"--auto-confirm								Ignore warning prompts provided by the transpiler (file overwriting warnings, etc)"
	]
	print("\n".join(help_list))

def tokenize_file(filename):
	file = File(filename)
	script_file = ScriptFile(filename)
	tokenizer = Tokenizer(file)
	tokenizer.tokenize(tree=script_file)
	print(script_file.to_script())

try:
	optionlist, args = getopt.getopt(sys.argv[1:], "hm", ["help", "minify", "no-comments"])
	for option, argument in optionlist:
		if option == "-h" or option == "--help":
			print_help()
		elif option == "-m" or option == "--minify":
			set_config("minify", True)
			set_config("nocomments", True)
		elif option == "--no-comments":
			set_config("nocomments", True)
except:
	print_help()

tokenize_file("test.egg")