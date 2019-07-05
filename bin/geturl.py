#!env python3

import argparse
import logging
import os
from git import Repo

def get_repo_from_url(url):
	(user, repo) = url.split(':')
	if repo.endswith('.git'):
		repo = repo[0:-4]
	return repo

def collect_all_rule_files(working_dir):
	rule_file_urls = []

	# this should really enumerate the repo files for lsrules rather than
	# the file system in case branches are different...
	for root, dirs, files in os.walk(working_dir, topdown=True):
		for name in files:
			if name.endswith('.lsrules'):
				path = os.path.join(root, name)          # get the full path
				path = path[len(working_dir):] # then remove the working directory
				rule_file_urls.append(path)

	return rule_file_urls

def main():
	parser = argparse.ArgumentParser(description='Get github raw URL for a specific file')
	parser.add_argument('--branch', dest='branch', action='store', default=None, help='Branch to use.  Current branch if unspecified.')
	parser.add_argument('-d', dest='debug', action='store_true', help='Print debug output')
	args = parser.parse_args()

	if args.debug:
		logging.basicConfig(level=logging.DEBUG)

	repo = Repo(".")
	repo_branch = repo.active_branch
	if args.branch != None:
		if args.branch not in repo.branches:
			print("Not a valid branch: " + args.branch)
			logging.warning("Not a valid branch: " + args.branch)
			return
		repo_branch = args.branch

	repo_name = get_repo_from_url(repo.remote().url)

	logging.debug("Repo Name: " + repo_name)
	logging.debug("Repo Branch: " + str(repo_branch))

	github_raw_url_base = "https://raw.githubusercontent.com/" + str(repo_name) + "/" + str(repo_branch)

	rule_files = collect_all_rule_files(repo.working_tree_dir)

	for file in rule_files:
		print(github_raw_url_base + file)

main()