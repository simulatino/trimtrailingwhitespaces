#!/usr/bin/env python

import string, sys

text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
_null_trans = string.maketrans("", "")

# test for text file
def istextfile(filename, blocksize = 512):
    return istext(open(filename).read(blocksize))

def istext(s):
    if "\0" in s:
        return 0
    
    if not s:  # Empty files are considered text
        return 1

    # Get the non-text characters (maps a character to itself then
    # use the 'remove' option to get rid of the text characters.)
    t = s.translate(_null_trans, text_characters)

    # If more than 30% non-text characters, then
    # this is considered a binary file
    # try to avoid integer division 
    if len(t) >= len(s) * 0.30:
        return 0
    return 1

# help message on usage
def usage(argv):
    print "\n Usage: %s  <directory> [<directory> ...]" % (argv[0],)
    print """
  Shows recursively which files in a directory are text
  and which are binary.

  If no directory is given, the current directory '.' 
  is used as default.
  """
 
# warning message for unkown options
def unkownOption(argv):
    print "Unknown option !" 
    print " Use %s -h [--help] for usage instructions." % (argv[0],)

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
                    print table[istextfile(fullname)], repr(fullname)[1:-1]
                except IOError:  # eg, this is a directory
                    pass    
    
if __name__ == "__main__":
    main(sys.argv)
