#!env python3

import json
import os;

script_dir = os.path.dirname(os.path.realpath(__file__))

root_dir = os.path.abspath(os.path.join(script_dir, os.pardir))


onlyfiles = [f for f in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir, f))]

for file in onlyfiles:
	path = os.path.join(root_dir, file)
	filename, file_extension = os.path.splitext(path)
	if file_extension == ".lsrules":
		data = json.load(open(path, 'r'))
		for rule in data["rules"]:
			if "creationDate" in rule.keys():
				del rule["creationDate"]
			if "modificationDate" in rule.keys():
				del rule["modificationDate"]

		json.dump(data, open(path, 'w'), indent=2)
