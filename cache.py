import json
import os
import math

cache = {}

def load_cache():
	try:
		os.mkdir("./.eggscript")
	except:
		pass

	try:
		global cache
		cache = json.load(open("./.eggscript/file_cache.json", "r"))
	except:
		print("Could not open cache.")

def add_to_cache(filename):
	global cache
	cache[filename] = math.floor(os.path.getmtime(filename))

def has_been_modified(filename):
	global cache
	if filename in cache and cache[filename] == math.floor(os.path.getmtime(filename)):
		return False
	else:
		return True

def save_cache():
	json.dump(cache, open("./.eggscript/file_cache.json", "w"))