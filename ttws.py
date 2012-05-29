#!/usr/bin/env python
"""Trimming of trailing white spaces.

Author-email: "Dietmar Winkler" <dietmar.winkler@dwe.no>

License: See UNLICENSE file

This script will recursively remove all trailing white spaces in all
text files in a given directory. Binary files and files residing in
version control specific directories are skipped.

As an addition one can also let it clean out obsolete or empty/superfluous
Modelica annotations from Modelica (`*.mo`) files.

It uses a binary tester based on the python magic implementation from
	Adam Hupp, http://hupp.org/adam/hg/python-magic

As a fallback (especially if libmagic is not available, like on Windows)
it acts only on files with a given file extension listed in 'extstring'.

"""
from __future__ import with_statement
from pyparsing import White, Keyword, nestedExpr, lineEnd, Suppress, ZeroOrMore, Optional, CharsNotIn, ParseException
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
		Usage: %s [OPTIONS] <directory> [<directory> ...]

		 This script will recursively remove all trailing white spaces in all
		 text files in a given list directories. Binary files and files residing in
		 '.bzr', '.cvs', '.git', '.hg', '.svn' directories are skipped.

		Note for Windows users:
		 If you have not libmagic installed the script will fallback to only
		 trim files with the following extensions: %s

		Options:
			-h, --help
				displays this help message

			-c, --clean
			        WARNING: USE THIS OPTION AT YOUR OWN RISK AS IT *WILL* BREAK YOUR CODE!
				Removes obsolete or superfluous annotation constructs
				from Modelica files. Only use this if your code is under version control
				and in combination with a careful code-diff review.
		""" % (os.path.split(args[0])[1],extstring,)
	print textwrap.dedent(message)

def unkownOption(args):
	"""Warning message for unknown options."""
	warning = """
		UNKNOWN OPTION: "%s"

		Use %s -h [--help] for usage instructions.
		""" % (args[1],args[0],)
	print textwrap.dedent(warning)

def unkownDirectory(args):
	"""Warning message for unknown Directory."""
	warning = """
	        WARNING: Ignoring unkown directory: "%s"
		""" % (args)
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
		else:
			unkownOption(args)
			sys.exit(0)

	# Walk through the given path and call trim function for text files only:
	for dirname in dirnames:
		if os.path.exists(dirname) is False:
			# Warn about an unknown directory
			unkownDirectory(dirname)
		else:
			for path, dirs, files in os.walk(dirname):
				for file in files:
					filepath = os.path.join(path, file)
					filetype = detecttype(filepath)
					if blacklisted(path):
						print "skipping version control file: "+filepath
					elif filetype is "mo" and cleanOpt is True:
						print "trimming and cleaning " + filepath
						trimWhitespace(filepath)
						cleanAnnotation(filepath)
					elif filetype is "mo" or filetype is "text":
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

def flatten(arg):
      ret = []
      for item in arg:
            if type(item)==list:
                  ret = ret + flatten(item)
            elif type(item)==tuple:
                  ret = ret + flatten(list(item))
            else:
                  ret.append(item)
      return ret

def skipNonEmptyGraphics(s, loc, tokens):
	flattened =  flatten(tokens.args[0].asList())
#	 print flattened
	graphicsPresent = False
	for substring in flattened:
		if substring.startswith('graphics'):
			if not substring.endswith('graphics'):
				graphicsPresent = True
	if graphicsPresent:
		raise ParseException('graphics defined, skipping...')

def cleanAnnotation(filepath):
	"""Clean out the obsolete or superflous annotations."""
	with open(filepath, 'r') as mo_file:
		string = mo_file.read()
		# remove 'Window(),' and 'Coordsys()' annotations:
		WindowRef = ZeroOrMore(White(' \t')) + (Keyword('Window')|Keyword('Coordsys')) + nestedExpr() + ',' + ZeroOrMore(White(' \t') + lineEnd)
		out = Suppress(WindowRef).transformString(string)
		# special care needs to be taken if the annotation is the last one
		WindowLastRef = Optional(',') + ZeroOrMore(White(' \t')) + (Keyword('Window')|Keyword('Coordsys')) + nestedExpr() + ZeroOrMore(White(' \t') + lineEnd)
		out = Suppress(WindowLastRef).transformString(out)

		# remove empty '[__Dymola_]experimentSetupOutput(),' annotation:
		expRef = Optional(',') +  ZeroOrMore(White(' \t')) +  Optional('__Dymola_') + (Keyword('experimentSetupOutput')|Keyword('experiment')|Keyword('DymolaStoredErrors')|Keyword('Diagram')|Keyword('Icon')) + ~nestedExpr() +  ~CharsNotIn(',)')
		out = Suppress(expRef).transformString(out)

		# Remove Icon and Diagram annotations that do not contain any graphics
		emptyRef =  ZeroOrMore(White(' \t')) + (Keyword('Icon')|Keyword('Diagram')) + nestedExpr()('args') + ',' + ZeroOrMore(White(' \t') + lineEnd)
		emptyRef.setParseAction(skipNonEmptyGraphics)
		out = Suppress(emptyRef).transformString(out)
		# special care for the last annotation again
		emptyRef =   Optional(',') + ZeroOrMore(White(' \t')) + (Keyword('Icon')|Keyword('Diagram')) + nestedExpr()('args') + ZeroOrMore(White(' \t') + lineEnd)
		emptyRef.setParseAction(skipNonEmptyGraphics)
		out = Suppress(emptyRef).transformString(out)

		# in case we end up with empty annotations remove them too
		AnnotationRef = ZeroOrMore(White(' \t')) + Keyword('annotation') + nestedExpr('(',');',content=' ') + ZeroOrMore(White(' \t') + lineEnd)
		out = Suppress(AnnotationRef).transformString(out)
	with open(filepath,'w') as mo_file:
		mo_file.write(out)

if __name__ == "__main__":
	sys.exit(main(sys.argv))
