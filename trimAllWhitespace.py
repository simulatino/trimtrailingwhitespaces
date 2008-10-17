"""Trimming of trailing white spaces

This script will recursively remove all trailing white spaces in all files
in a given directory. Files residing in '.svn' or '.git' directories are
excluded.

Usage: 	python trimAllWhitespace.py <DestinationDir>
"""

import os, sys

def main(args):
	for path, dirs, files in os.walk(args[1]):
		for file in files:
			if not ".svn" in path and not ".git" in path:
				fullname = os.path.join(path, file)
				trimWhitespace(fullname)
			else:
				print "excluding " + fullname # DEBUG

def trimWhitespace(filepath):
	lines = []
	for line in open(filepath, "r"):
		lines.append(line.rstrip())
	f = open(filepath, "w")
	f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
	sys.exit(main(sys.argv))
