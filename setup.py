"""Setup script to generate a Windows executable.

Author-email: "Dietmar Winkler" <dietmarw at gmx de>

License: See UNLICENSE file

Usage: python setup.py py2exe

Prerequisites: py2exe from www.py2exe.org

"""
from distutils.core import setup
import py2exe

setup(console=['ttws.py'])
