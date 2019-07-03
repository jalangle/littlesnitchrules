#!env python3

import json

# filters explained here:
# https://adblockplus.org/en/filter-cheatsheet#blocking2

input_file = open("easylist.txt")

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

print(json.dumps(output_data, indent=4))
