"""Setup script to generate a Windows executable.

Author-email: "Dietmar Winkler" <dietmarw at gmx de>

License: See UNLICENSE file

Usage: python setup.py py2exe

Prerequisites: py2exe from www.py2exe.org

"""
from distutils.core import setup
import py2exe

setup(
    console=['ttws.py'],
    name = 'ttws',
    version = 0.2,
    description = 'Script to remove trailing whitespaces from textfiles.',
    author = 'Dietmar Winkler',
    author_email = 'http://claimid/dietmarw',
    platforms = 'Posix; MacOS X; Windows',
    packages = find_packages(exclude=['test']),
    include_package_data = True
    )
