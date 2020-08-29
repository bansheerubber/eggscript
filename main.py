from config import set_config, get_config, add_exported_lines, add_read_file
from file import File
from tokenizer import Tokenizer
from time import time
from script_file import ScriptFile

from pathlib import Path
import os
import sys, getopt

def print_help():
	help_list = ["Syntax:   eggscript [options] [files or directory]",
		"Examples: eggscript server.egg",
	  "	  eggscript server.egg -o server.cs",
	  "	  eggscript server.egg -o ./Server_Minigame",
	  "	  eggscript ./Server_Minigame-dev -o ../Server_Minigame -m --no-warnings",
		"",
		"Options:",
		"-h, --help								Show help message",
		"-o [directory], --output [directory]					Output transpiled TorqueScript file(s) to the specified file or directory. Filenames are preserved by default (server.egg turns into server.cs, example.egg turns into server.cs) if output is a directory.",
		"-f [expression], --file-replace [expression]				Renames output files. Example: -f \"{}.1.cs\" will export all files withe the \".1.cs\" extension. -f \"new_{}.cs\" will export all files with \"new_\" prepended infront of the file name. Default file replace is \"{}.cs\".",
		"-m, --minify								Minify the output files (pretty prints by default)",
		"-c, --include-cs							Include .cs files in addition to .egg files",
		"-v, --verbose 								Verbose output",
		"--no-comments								Do not output comments",
		"--no-warnings								Do not print warnings",
		"--auto-confirm								Ignore warning prompts provided by the transpiler (file overwriting warnings, etc)"
	]
	print("\n".join(help_list))

def scan_directory(directory, output_directory="./", file_replacement="{}.cs"):
	original_path = Path(directory)
	for root, subdirs, files in os.walk(directory):
		root_path = Path(root)
		for filename in files:
			path = Path(f"{root}/{filename}")
			if path.suffix == ".egg" or (get_config("includecs") and path.suffix == ".cs"):
				true_output_directory = output_directory + root_path.absolute().__str__().replace(original_path.absolute().__str__(), "")
				transpile_file(f"{root}/{filename}", output_directory=true_output_directory, file_replacement=file_replacement)

def transpile_file(filename, output_directory="./", file_replacement="{}.cs"):
	path = Path(filename)

	if get_config("verbose") == True:
		print(f"Parsing '{path.absolute()}'")
	
	file = File(filename)
	script_file = ScriptFile(filename)
	tokenizer = Tokenizer(file)
	tokenizer.tokenize(tree=script_file)
	script = script_file.to_script()

	output_filename = ""
	try:
		output_filename = file_replacement.format(path.stem)
	except:
		print(f"Could not format file using '{file_replacement}'")
		return

	output = Path(f"{output_directory}/{output_filename}")

	try:
		output.parent.mkdir()
	except:
		pass

	file = open(output.absolute(), "w")
	file.write(script)
	add_exported_lines(script.count("\n") + 1)
	add_read_file()
	file.close()

optionlist, args = getopt.getopt(sys.argv[1:], "hmcvo:f:", ["help", "minify", "no-comments", "output=", "file-replace=", "include-cs", "verbose"])

if len(args) > 0:
	set_config("output", "./")
	set_config("filereplace", "{}.cs")
	set_config("includecs", False)
	
	for option, argument in optionlist:
		if option == "-h" or option == "--help":
			print_help()
		elif option == "-m" or option == "--minify":
			set_config("minify", True)
			set_config("nocomments", True)
		elif option == "-o" or option == "--output":
			set_config("output", argument)
		elif option == "-f" or option == "--file-replace":
			set_config("filereplace", argument)
		elif option == "-c" or option == "--include-cs":
			set_config("includecs", True)
		elif option == "-v" or option == "--verbose":
			set_config("verbose", True)
		elif option == "--no-comments":
			set_config("nocomments", True)

	# go through args and figure out what to do with them
	for arg in args:
		if os.path.exists(arg):
			start = time()
			
			if os.path.isdir(arg):
				scan_directory(arg, output_directory=get_config("output"), file_replacement=get_config("filereplace"))
			else:
				transpile_file(arg, output_directory=get_config("output"), file_replacement=get_config("filereplace"))
			
			parsed_lines = get_config("parsedlines")
			exported_lines = get_config("exportedlines")
			number_of_files = get_config("readfiles")
			time_taken = "{:.2f}".format(round(time() - start, 2))
			print(f"Read {number_of_files} files, parsed {parsed_lines} lines and exported {exported_lines} lines in {time_taken} seconds")
		else:
			if "-" in arg:
				print(f"Failed to read file or directory '{arg}' (are options before files and directories? eggscript [options] [files or directory])")
			else:
				print(f"Failed to read file or directory '{arg}'")
else:
	print_help()