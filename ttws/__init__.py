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
from __future__ import absolute_import, with_statement

import os
import textwrap

from pyparsing import (White, Keyword, nestedExpr, lineEnd, Suppress,
        ZeroOrMore, Optional, CharsNotIn, ParseException, CaselessLiteral)


# For Windows: list of file extensions to apply the script on
# (including the dot and separated by a comma)
extstring = ".mo,.mos,.c,.h,.cpp,.txt"

# list of version control directories to ignore
BLACKLIST = ['.bzr', '.cvs', '.git', '.hg', '.svn', '.#']

# convert the string object to a list object
listofexts  = extstring.split(",")

def unkownOption(script_name, args):
    """Warning message for unknown options."""
    warning = """
        UNKNOWN OPTION: "%s"

        Use %s -h [--help] for usage instructions.
        """ % (args,script_name,)
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
        from .magic import Magic
        mime = Magic(mime=True)
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

def trimWhitespace(filepath):
    """Trim trailing white spaces from a given filepath."""
    lines = []
    with open(filepath, "rb") as f:
        for line in f:
            lines.append(line.rstrip())
    data = "\n".join(lines) + "\n"
    newdata = data.replace("\r\n", "\n")
    with open(filepath, "wb") as f:
        f.write(newdata)

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
    graphicsPresent = False
    for substring in flattened:
        if substring.startswith('graphics'):
            if not substring.endswith('graphics'):
                graphicsPresent = True
    if graphicsPresent:
        raise ParseException('graphics defined, skipping...')

def cleanAnnotation(filepath):
    """Clean out the obsolete or superflous annotations."""
    with open(filepath, 'rb') as mo_file:
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
    with open(filepath,'wb') as mo_file:
        mo_file.write(out)

def stripDocString(filepath):
    """Clean out the obsolete or superflous annotations."""
    with open(filepath, 'rb') as mo_file:
        string = mo_file.read()

        # define expressions to match leading and trailing
        # html tags, and just suppress the leading or trailing whitespace
        opener = White().suppress() + CaselessLiteral("<html>")
        closer = CaselessLiteral("</html>") + White().suppress()

        # define a single expression to match either opener
        # or closer - have to add leaveWhitespace() call so that
        # we catch the leading whitespace in opener
        either = opener|closer
        either.leaveWhitespace()
        out = either.transformString(string)

    with open(filepath,'wb') as mo_file:
        mo_file.write(out)
