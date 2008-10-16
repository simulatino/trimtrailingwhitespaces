#!/usr/bin/env python

import string, sys, magic, textwrap

# you need python bindings for magic installed in oder to run this
ms = magic.open(magic.MAGIC_MIME)
ms.load()

# detect the mime type of the text file
def detecttype(filename):
	type = ms.file(filename)
	if "text/" in type:
		return "text"
	else:
		return type

# help message on usage
def usage(argv):
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
	print textwrap.dedent(message)

# warning message for unkown options
def unkownOption(argv):
	warning = """
		UNKNOWN OPTION: "%s"

		Use %s -h [--help] for usage instructions.
		""" % (argv[1],argv[0],)
	print textwrap.dedent(warning)

def main(argv):
	import os, getopt
	# look for optional arguments
	try:
		opts, dirnames = getopt.getopt(argv[1:], "h", ["help"])
	# unkown option is given trigger the display message
	except getopt.GetoptError:
		unkownOption(argv)
		sys.exit(0)
	table = {0: "binary", 1: "text"}
	for o, a in opts:
		if o == "-h" or "--help":
			usage(argv)
			sys.exit(0)
		else:
			unkownOption(argv)
			sys.exit(0)
	# default directory
	if not dirnames:
		dirnames = ["."]
	# walk recursively through the given directories
	for dirname in dirnames:
		for path, dirs, files in os.walk(dirname):
			for file in files:
				fullname = os.path.join(path, file)
				try:
					print detecttype(fullname),":", repr(fullname)[1: - 1]
				except IOError:  # eg, this is a directory
					pass

if __name__ == "__main__":
	sys.exit(main(sys.argv))
