"""Setup script to generate an stand-alone executable.

Author-email: "Dietmar Winkler" <dietmar.winkler@dwe.no>

License: See UNLICENSE file

Usage: Run the build process by running the command 'python setup.py build'
       If everything works well you should find a subdirectory in the build
       subdirectory that contains the files needed to run the script
       without Python

"""
import sys

from setuptools import setup, find_packages


setup(
#   console=['ttws.py'],
    name = 'ttws',
    version = 0.3,
    description = 'Script to remove trailing whitespaces from textfiles.',
    author = 'Dietmar Winkler',
    author_email = 'http://claimid/dietmarw',
    platforms = 'Posix; MacOS X; Windows',
    )
