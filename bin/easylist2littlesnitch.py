#!env python3

import argparse
import io
import json
import requests

def get_easylist_file(input_path):
	if input_path == None:
		url = "https://easylist.to/easylist/easylist.txt"
		response = requests.get(url)
		return io.StringIO(response.text)
	else:
		return open(args.input_path, 'r')

def dump_data(output_path, output_data):
	if(output_path == None):
		print(json.dumps(output_data, indent=2))
	else:
		output_file = open(output_path, 'w')
		json.dump(output_data, output_file, indent=2)
		output_file.close()

def main():
	parser = argparse.ArgumentParser(description='Turn domains from an AdBlock formatted filter list into a littlesnitch lsrules file')
	parser.add_argument('--input', dest='input_path', action='store', default=None, help='Path to an AdBlock filter formatted file')
	parser.add_argument('--output', dest='output_path', action='store', default=None, help='Path to output file')
	args = parser.parse_args()

	blocked_domains = {};
	input_file = get_easylist_file(args.input_path)

	# filters explained here:
	# https://adblockplus.org/en/filter-cheatsheet#blocking2
	with get_easylist_file(args.input_path) as input_file:
		for line in input_file:
			line = line.strip()

			# starting with || is a domain rule
			if line.startswith("||"):
				line = line[2:]
				separator = line.find("^")

				# if we find a separator, then this is a rule where
				# we block if the domain contains this.  i.e  example.com blocks this.example.com
				if separator != -1:
					blocked_domains[line[:separator]] = 1

	output_data = {}
	output_data["description"] = "Blocking domains based on easylist"
	output_data["name"] = "EasyList"
	output_data["rules"] = [];

	for domain in blocked_domains.keys():
		deny_rule = {}
		deny_rule["action"] = "deny"
		deny_rule["owner"] = "me"
		deny_rule["process"] = "any"
		deny_rule["remote-domains"] = domain
		output_data["rules"].append(deny_rule)

	dump_data(args.output_path, output_data)

main()