#!/usr/bin/env python
"""Trimming of trailing white spaces.

Author-email: "Dietmar Winkler" <dietmarw at gmx de>

License: See UNLICENSE file

This script will recursively remove all trailing white spaces in all
text files in a given directory. Binary files and files residing in
'.svn' or '.git' directories are skipped.

It uses a binary tester based on the python magic implementation from
	Adam Hupp, http://hupp.org/adam/hg/python-magic

As a fallback (especially if libmagic is not available, like on Windows)
it acts only on files with a given file extension listed in 'extstring'.

"""

import os
import sys
import textwrap

# For Windows: list of file extensions to apply the script on
# (including the dot and separated by a comma)
extstring = ".mo,.mos,.c,.h,.cpp,.txt"

# list of version control directories to ignore
BLACKLIST = ['.bzr', '.cvs', '.git', '.hg', '.svn']

# convert the string object to a list object
listofexts  = extstring.split(",")

def usage(args):
	"""Help message on usage."""
	message = """
		Usage: %s [OPTIONS] <directory>

		 This script will recursively remove all trailing white spaces in all
		 text files in a given directory. Binary files and files residing in
		 '.bzr', '.cvs', '.git', '.hg', '.svn' directories are skipped.

		Note for Windows users:
		 If you have not libmagic installed the script will fallback to only
		 trim files with the following extensions: %s

		Options:
			-h, --help
				displays this help message

			-c, --clean
			        removes obsolete or superfluous annotation constructs
				from Modelica files.
				WARNING: USE THIS OPTION AT YOUR OWN RISK!
		""" % (os.path.split(args[0])[1],extstring,)
	print textwrap.dedent(message)

def unkownOption(args):
	"""Warning message for unknown options."""
	warning = """
		UNKNOWN OPTION: "%s"

		Use %s -h [--help] for usage instructions.
		""" % (args[1],args[0],)
	print textwrap.dedent(warning)

def detecttype(filepath):
	"""Detect the mime type of the text file."""
	try:
		import magic
		mime = magic.Magic(mime=True)
		type = mime.from_file(filepath)
		root, ext = os.path.splitext(filepath)
		if ext in '.mo':
			return "mo"
		elif "text/" in type:
			return "text"
		else:
			return type
	except (ImportError, TypeError):
		root, ext = os.path.splitext(filepath)
		if ext in '.mo':
			return "mo"
		elif ext in listofexts:
			return "text"
		else:
			return "unknown"

def main(args):
	import getopt
	# Look for optional arguments:
	try:
		opts, dirnames = getopt.getopt(args[1:], "hc", ["help","clean"])
	# Unknown option is given trigger the display message:
	except getopt.GetoptError:
		unkownOption(args)
		sys.exit(0)
	# if no dir name is given print the usage message
	if not dirnames:
		usage(args)
		sys.exit(0)

	# If help option is given display help otherwise display warning:
	cleanOpt = False
	for opt, arg in opts:
		if opt in ("-h","--help"):
			usage(args)
			sys.exit(0)
		elif opt in ("-c","--clean"):
			cleanOpt = True
			print cleanOpt #FIXME output for debugging
#			sys.exit(0)
		else:
			unkownOption(args)
			sys.exit(0)

	# Walk through the given path and call trim function for text files only:
	for path, dirs, files in os.walk(args[1]):
		for file in files:
			filepath = os.path.join(path, file)
			filetype = detecttype(filepath)
			if blacklisted(path):
				print "skipping version control file: "+filepath
			elif filetype is "mo" and cleanOpt is True:
				print "trimming and cleaning" + filepath
				trimWhitespace(filepath)
				cleanAnnotation(filepath)
			elif filetype is "mo" or "text":
				print "trimming " + filepath
				trimWhitespace(filepath)
			else:
				print "skipping file of type "+filetype+": "+filepath
def blacklisted(path):
	"""
	determines whether the given path contains a blacklisted directory
	"""
	for dirname in path.split(os.sep):
		if dirname in BLACKLIST:
			return True
	return False

def trimWhitespace(filepath):
	"""Trim trailing white spaces from a given filepath."""
	lines = []
	for line in open(filepath, "r"):
		lines.append(line.rstrip())
	f = open(filepath, "w")
	f.write("\n".join(lines) + "\n")
	f.close

def cleanAnnotation(filepath):
	"""Clean out the obsolete or superflous annotations."""
	with open(filepath, 'r') as mo_file:
		string = mo_file.read()
		# for now we only remove 'Window()' annotations:
		WindowRef = ZeroOrMore(White(' \t')) + Keyword('Window') + nestedExpr() + ',' + ZeroOrMore(White(' \t') + lineEnd)
		out = Suppress(WindowRef).transformString(string)
	with open(filepath,'w') as mo_file:
		mo_file.write(out)

if __name__ == "__main__":
	sys.exit(main(sys.argv))
