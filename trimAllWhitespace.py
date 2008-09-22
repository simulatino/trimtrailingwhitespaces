"""Trimming of trailing white spaces

This script will recursively remove all trailing white spaces in all files
in a given directory. Files residing in '.svn' or '.git' directories are 
excluded.

Usage: 	python trimAllWhitespace.py <DestinationDir>
"""
__version__ = "$Revision: $"
__date__ = "$Date: $"
__license__ = "Modelica"

import sys
import os

def main(args):
    for path, dirs, files in os.walk(args[1]):
        for file in files:
            if not path.endswith(".svn") and not path.endswith(".git"):
                trimWhitespace(addTrailingSlash(path) + file)
            else:
                print "excluding " + addTrailingSlash(path) + file # DEBUG

def trimWhitespace(filepath):
    lines = []
    for line in open(filepath, "r"):
        lines.append(line.rstrip())
    f = open(filepath, "w")
    f.write("\n".join(lines))

def addTrailingSlash(path):
    if path[-1] != os.sep:
        path = path + os.sep
    return path

if __name__ == "__main__":
    sys.exit(main(sys.argv))
