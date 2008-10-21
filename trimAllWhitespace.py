#!/usr/bin/env python
"""Trimming of trailing white spaces.

This script will recursively remove all trailing white spaces in all
text files in a given directory. Binary files and files residing in
'.svn' or '.git' directories are skipped.

It uses a binary tester based on the python magic implementation from
	Adam Hupp, http://hupp.org/adam/hg/python-magic

"""

import os
import sys
import textwrap

import magic

mime = magic.Magic(mime=True)

def usage(args):
	"""Help message on usage."""
	message = """
		Usage: python %s [OPTIONS] <directory>

		 This script will recursively remove all trailing white spaces in all
		 text files in a given directory. Binary files and files residing in
		 '.svn' or '.git' directories are skipped.

		Options:
			-h, --help
				displays this help message
		""" % (args[0],)
	print textwrap.dedent(message)

def unkownOption(args):
	"""Warning message for unkown options."""
	warning = """
		UNKNOWN OPTION: "%s"

		Use %s -h [--help] for usage instructions.
		""" % (args[1],args[0],)
	print textwrap.dedent(warning)

def detecttype(filepath):
	"""Detect the mime type of the text file."""
	type = mime.from_file(filepath)
	if "text/" in type:
		return "text"
	else:
		return type

def main(args):
	import getopt
	# Look for optional arguments:
	try:
		opts, dirnames = getopt.getopt(args[1:], "h", ["help"])
	# Unkown option is given trigger the display message:
	except getopt.GetoptError:
		unkownOption(args)
		sys.exit(0)

	# If help option is given display help otherwise display warning:
	for o, a in opts:
		if o == "-h" or "--help":
			usage(args)
			sys.exit(0)
		else:
			unkownOption(args)
			sys.exit(0)

	# Walk through the given path and call trim function for text files only:
	for path, dirs, files in os.walk(args[1]):
		for file in files:
			filepath = os.path.join(path, file)
			filetype=detecttype(filepath)
			if ".svn" in path or ".git" in path:
				print "skipping version control file: "+filepath
			elif filetype=="text":
				print "trimming " + filepath
				trimWhitespace(filepath)
			else:
				print "skipping binary file of type "+filetype+": "+filepath

def trimWhitespace(filepath):
	"""Trim trailing white spaces from a given filepath."""
	lines = []
	for line in open(filepath, "r"):
		lines.append(line.rstrip())
	f = open(filepath, "w")
	f.write("\n".join(lines) + "\n")
	f.close

if __name__ == "__main__":
	sys.exit(main(sys.argv))
