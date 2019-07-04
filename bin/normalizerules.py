#!env python3

import json
import os;

def is_lsrules_file(path):
	filename, file_extension = os.path.splitext(path)
	return os.path.isfile(path) and file_extension == ".lsrules"

def normalize_file(path):
	filename, file_extension = os.path.splitext(path)
	if file_extension == ".lsrules":
		data = json.load(open(path, 'r'))
		for rule in data["rules"]:
			if "creationDate" in rule.keys():
				del rule["creationDate"]
			if "modificationDate" in rule.keys():
				del rule["modificationDate"]

		json.dump(data, open(path, 'w'), indent=2)

def main():
	script_dir = os.path.dirname(os.path.realpath(__file__))
	root_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

	onlyfiles = [f for f in os.listdir(root_dir) if is_lsrules_file(os.path.join(root_dir, f))]

	for file in onlyfiles:
		normalize_file(os.path.join(root_dir, file))

main()