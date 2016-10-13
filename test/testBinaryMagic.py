#!/usr/bin/env python
"""Test script that displayes the type of a file.

Author-email: "Dietmar Winkler" <dietmarw at gmx de>

License: See UNLICENSE file

This binary tester uses the python magic implementation from
Adam Hupp, http://hupp.org/adam/hg/python-magic

"""

import os
import sys
import textwrap

import magic

mime = magic.Magic(mime=True)

def detecttype(filename):
	"""Detect the mime type of the file"""
	type = mime.from_file(filename)
	if "text/" in type:
		return "text"
	else:
		return type

def usage(argv):
	"""Help message on usage."""
	message = """
		Usage: %s [OPTIONS] <directory> [<directory> ...]

		 Shows recursively which files in a directory are text
		 and which are binary or other formats

		 If no directory is given, the current directory '.'
		 is used as default.

		Options:
			-h, --help
				displays this help message
		""" % (argv[0],)
	print(textwrap.dedent(message))

# warning message for unkown options
def unkownOption(argv):
	"""Warning message for unkown options."""
	warning = """
		UNKNOWN OPTION: "%s"

		Use %s -h [--help] for usage instructions.
		""" % (argv[1],argv[0],)
	print(textwrap.dedent(warning))

def main(argv):
	import getopt
	# Look for optional arguments:
	try:
		opts, dirnames = getopt.getopt(argv[1:], "h", ["help"])
	# Unkown option is given trigger the display message:
	except getopt.GetoptError:
		unkownOption(argv)
		sys.exit(0)
	for o, a in opts:
		if o == "-h" or "--help":
			usage(argv)
			sys.exit(0)
		else:
			unkownOption(argv)
			sys.exit(0)
	# Default directory:
	if not dirnames:
		dirnames = ["."]
	# Walk recursively through the given directories:
	for dirname in dirnames:
		for path, dirs, files in os.walk(dirname):
			for file in files:
				fullname = os.path.join(path, file)
				try:
					print detecttype(fullname),":", repr(fullname)[1: - 1]
				except IOError:
					pass

if __name__ == "__main__":
	sys.exit(main(sys.argv))
