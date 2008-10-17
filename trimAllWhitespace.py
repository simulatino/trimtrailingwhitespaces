"""Trimming of trailing white spaces

This script will recursively remove all trailing white spaces in all files
in a given directory. Files residing in '.svn' or '.git' directories are
excluded.

Usage: 	python trimAllWhitespace.py <DestinationDir>
"""

import os, sys, magic, textwrap

mime = magic.Magic(mime=True)

# detect the mime type of the text file
def detecttype(filepath):
	type = mime.from_file(filepath)
	if "text/" in type:
		return "text"
	else:
		return type
# walk through the given path and call trim function for text files
def main(args):
	for path, dirs, files in os.walk(args[1]):
		for file in files:
			filepath = os.path.join(path, file)
			filetype=detecttype(filepath)
			if not ".svn" in path and not ".git" in path and filetype=="text":
				print "trimming " + filepath
				trimWhitespace(filepath)
			else:
				print "skipping binary file of type " +filetype + ": "+ filepath

# trim trailing white spaces from a given filepath
def trimWhitespace(filepath):
	lines = []
	for line in open(filepath, "r"):
		lines.append(line.rstrip())
	f = open(filepath, "w")
	f.write("\n".join(lines) + "\n")
	f.close

if __name__ == "__main__":
	sys.exit(main(sys.argv))
