import sys
import os
import getopt

from . import extstring, textwrap, detecttype


def main(args=None):
    if args is None:
        args = sys.argv

    script_name = args.pop(0)
    script_name = os.path.split(script_name)[1]

    # Look for optional arguments:
    try:
        opts, dirnames = getopt.getopt(args, "hsc", ["help","strip","clean"])
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
    stripOpt = False
    for opt, arg in opts:
        if opt in ("-h","--help"):
            usage(args)
            sys.exit(0)
        elif opt in ("-c","--clean"):
            cleanOpt = True
        elif opt in ("-s","--strip"):
            stripOpt = True
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
                for directory in dirs:
                    if directory in BLACKLIST:
                        print "skipping version control dir: %s " % directory
                        dirs.remove(directory)
                for file in files:
                    filepath = os.path.join(path, file)
                    filetype = detecttype(filepath)
                    if filetype is "mo" and cleanOpt is True:
                        print "trimming and cleaning %s" % filepath
                        trimWhitespace(filepath)
                        cleanAnnotation(filepath)
                    elif filetype is "mo" and stripOpt is True:
                        print "trimming and stripping %s" % filepath
                        trimWhitespace(filepath)
                        stripDocString(filepath)
                    elif filetype is "mo" or filetype is "text":
                        print "trimming %s" % filepath
                        trimWhitespace(filepath)
                    else:
                        print "skipping file of type %s: %s" % (filetype, filepath)


def usage(script_name):
    """Help message on usage."""
    message = """
        Usage: %s [OPTIONS] <directory> [<directory> ...]

         This script will recursively remove all trailing white spaces in all
         text files in a given list directories. Binary files and files residing in
         '.bzr', '.cvs', '.git', '.hg', '.svn' directories are skipped.

        Note for Windows users:
         If you do not have libmagic installed, the script will fall back to
         only trim files with the following extensions: %s

        Options:
            -h, --help
                displays this help message

            -s, --strip
                strips leading or trailing white spaces from info or
                revision strings that contain HTML documentation
                (those disturb the proper HTML rendering in 'some' tools)

            -c, --clean
                WARNING: USE THIS OPTION AT YOUR OWN RISK AS IT *WILL* BREAK YOUR CODE!
                Removes obsolete or superfluous annotation constructs
                from Modelica files. Only use this if your code is under version control
                and in combination with a careful code-diff review.
        """ % (script_name,extstring,)
    print textwrap.dedent(message)


if __name__ == "__main__":
    sys.exit(main())
