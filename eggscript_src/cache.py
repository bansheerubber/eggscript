import json
import os
import math
from eggscript_src.config import get_config

cache = {}
cache_options = []

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
	
	if should_reset_cache():
		if get_config("verbose") == True:
			print("Reset cache b/c arguments not the same")
		
		cache = {}

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
	save_cache_options()
	json.dump(cache, open("./.eggscript/file_cache.json", "w"))

def add_cache_option(config_option):
	global cache_options
	cache_options.append((config_option, get_config(config_option)))

def save_cache_options():
	global cache_options
	cache["config"] = cache_options

def get_option_from_tuple(desired_option_name, array):
	for option_name, option_value in array:
		if option_name == desired_option_name:
			return option_value
	return None

def should_reset_cache():
	global cache_options
	
	if "config" not in cache:
		cache["config"] = []
	
	if get_config("force") == True:
		return True
	
	if len(cache["config"]) != len(cache_options):
		return True
	else:
		list1 = sorted(cache["config"])
		list2 = sorted(cache_options)
		
		# go though cache options and make sure we have everything
		for option_name, option_value in list1:
			if get_option_from_tuple(option_name, list2) != option_value:
				print(list2[option_name], "!=", option_value)
				return True
		
		return False