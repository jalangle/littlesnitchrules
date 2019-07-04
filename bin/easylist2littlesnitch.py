#!env python3

import argparse
import json

parser = argparse.ArgumentParser(description='Turn domains from an AdBlock formatted filter list into a littlesnitch lsrules file')
parser.add_argument('--input', required=True, dest='input_path', action='store', default=None, help='Path to an AdBlock filter formatted file')
parser.add_argument('--output', dest='output_path', action='store', default=None, help='Path to output file')
args = parser.parse_args()

# filters explained here:
# https://adblockplus.org/en/filter-cheatsheet#blocking2

input_file = open(args.input_path, 'r')

output_data = {}
output_data["description"] = "Blocking domains based on easylist"
output_data["name"] = "EasyList"
output_data["rules"] = [];

for line in input_file:
	line = line.strip()

	# starting with || is a domain rule
	if line.startswith("||"):
		line = line[2:]
		separator = line.find("^")

		# if we find a separator, then this is a rule where 
		# we block if the domain contains this.  i.e  example.com blocks this.example.com
		if separator != -1:
			deny_rule = {}
			deny_rule["action"] = "deny"
			deny_rule["owner"] = "me"
			deny_rule["process"] = "any"
			deny_rule["remote-domains"] = line[:separator]
			output_data["rules"].append(deny_rule)

input_file.close()

if(args.output_path == None):
	print(json.dumps(output_data, indent=2))
else:
	output_file = open(args.output_path, 'w')
	json.dump(output_data, output_file, indent=2)
	output_file.close()
