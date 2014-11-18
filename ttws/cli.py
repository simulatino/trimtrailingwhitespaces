import sys
import os
import getopt
import textwrap

from . import (BLACKLIST, cleanAnnotation, extstring, detecttype,
               stripDocString, trimWhitespace, normalizeEOF, unknownDirectory,
               unknownOption)

def main(args=None):
    if args is None:
        args = sys.argv

    script_name = args.pop(0)
    script_name = os.path.split(script_name)[1]

    # Look for optional arguments:
    try:
        opts, dirnames = getopt.getopt(args, "hsc", ["help","strip","clean",
                                                     "eof","eol="])
    # If unknown option is given trigger the display message:
    except getopt.GetoptError:
        unknownOption(args)
        sys.exit(0)
    # if no dir name is given print the usage message
    if not dirnames:
        usage(args)
        sys.exit(0)

    # If help option is given display help otherwise display warning:
    cleanOpt = False
    stripOpt = False
    eofOpt = False
    eol = os.linesep
    for opt, arg in opts:
        if opt in ("-h","--help"):
            usage(args)
            sys.exit(0)
        elif opt in ("-c","--clean"):
            cleanOpt = True
        elif opt in ("-s","--strip"):
            stripOpt = True
        elif opt in ("--eof"):
            eofOpt = True
        elif opt in ("--eol"):
            eol = {
                "CRLF": "\r\n",
                "LF": "\n",
                "CR": "\r"
            }
            eol = eol.get(arg, os.linesep)
        else:
            unknownOption(args)
            sys.exit(0)

    # Walk through the given path and call trim function for text files only:
    for dirname in dirnames:
        if os.path.exists(dirname) is False:
            # Warn about an unknown directory
            unknownDirectory(dirname)
        else:
            for path, dirs, files in os.walk(dirname):
                for directory in dirs:
                    if directory in BLACKLIST:
                        print("skipping version control dir: %s " % directory)
                        dirs.remove(directory)
                for file in files:
                    filepath = os.path.join(path, file)
                    filetype = detecttype(filepath)
					# --help and empty opts have been handled before
                    if filetype is "mo" and cleanOpt is True:
                        print("trimming and cleaning %s" % filepath)
                        trimWhitespace(filepath, eol)
                        cleanAnnotation(filepath, eol)
                    elif filetype is "mo" and stripOpt is True:
                        print("trimming and stripping %s" % filepath)
                        trimWhitespace(filepath, eol)
                        stripDocString(filepath, eol)
                    elif filetype is "mo" and eofOpt is True:
                        print("trimming and normalizing EOF for %s" % filepath)
                        trimWhitespace(filepath, eol)
                        normalizeEOF(filepath, eol)
                    elif filetype is "mo" or filetype is "text":
                        print("trimming %s" % filepath)
                        trimWhitespace(filepath, eol)
                    else:
                        print("skipping file of type %s: %s" % (filetype, filepath))


def usage(script_name):
    """Help message on usage."""
    message = """
        Usage: ttws [OPTIONS] <directory> [<directory> ...]

         This script will recursively remove all trailing white spaces in all
         text files in a given list directories. Binary files and files residing in
         '.bzr', '.cvs', '.git', '.hg', '.svn' directories are skipped.

         Since the main application is for Modelica projects it expects all files
         to be of type ASCII or UTF8. Otherwise it will throw an exception,
         report the illegal file and terminate.

        Note for Windows users:
         If you do not have libmagic installed, the script will fall back to
         only trim files with the following extensions:
             %s

        Options:
            -h, --help
                displays this help message

            -s, --strip
                strips leading or trailing white spaces from info or
                revision strings that contain HTML documentation
                (those disturb the proper HTML rendering in 'some' tools)
				
            --eof
                normalizes the end of file so that it ends with a single empty
                newline

            --eol=[CRLF|LF|CR]
                Force the line endings to be of type:
                 - CRLF = '\\r\\n' Windows
                 - LF = '\\n' POSIX
                 - CR = '\\r' Mac (pre OSX)
                If empty or not specified it is set to the OS default.
                I.e., on this machine to: %s.

            -c, --clean
                WARNING: USE THIS OPTION AT YOUR OWN RISK AS
                         IT *MIGHT* BREAK YOUR CODE!
                Removes obsolete or superfluous annotation constructs
                from Modelica files.
                Only use this if your code is under version control
                and in combination with a careful code-diff review.

        """ % (extstring, repr(os.linesep))
    print(textwrap.dedent(message))


if __name__ == "__main__":
    sys.exit(main())
