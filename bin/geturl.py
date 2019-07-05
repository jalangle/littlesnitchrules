#!env python3

import argparse
import os
from git import Repo

def get_repo_from_url(url):
	(user, repo) = url.split(':')
	if repo.endswith('.git'):
		repo = repo[0:-4]
	return repo

def collect_all_rule_files(working_dir):
	rule_file_urls = []

	for root, dirs, files in os.walk(working_dir, topdown=True):
		for name in files:
			if name.endswith('.lsrules'):
				path = os.path.join(root, name)          # get the full path
				path = path[len(working_dir):] # then remove the working directory
				rule_file_urls.append(path)

	return rule_file_urls

def main():
	repo = Repo(".")
	origin = repo.remote()
	repo_name = get_repo_from_url(origin.url)
	repo_branch = repo.active_branch

	github_raw_url_base = "https://raw.githubusercontent.com/" + str(repo_name) + "/" + str(repo_branch)

	rule_files = collect_all_rule_files(repo.working_tree_dir)

	for file in rule_files:
		print(github_raw_url_base + file)

main()