"""Setup script to generate an stand-alone executable.

Author-email: "Dietmar Winkler" <dietmar.winkler@dwe.no>

License: See UNLICENSE file

Usage: Run the build process by running the command 'python setup.py build'
       If everything works well you should find a subdirectory in the build
       subdirectory that contains the files needed to run the script

"""

from setuptools import setup, find_packages


CLASSIFIERS = """
Environment :: Console
Intended Audience :: Developers
Operating System :: OS Independent
Programming Language :: Python :: 2
Programming Language :: Python :: 3
""".strip().splitlines()

META = {
    'name': 'ttws',
    'url': 'https://github.com/simulatino/trimtrailingwhitespaces',
    'version': '0.8.5',
    'description': 'Script to remove trailing whitespaces from textfiles and more.',
    'classifiers': CLASSIFIERS,
    'license': 'UNLICENSE',
    'author': 'Dietmar Winkler',
    'author_email': 'dietmar.winkler@dwe.no',
    'packages': find_packages(exclude=['test']),
    'entry_points': {
        'console_scripts': 'ttws = ttws.cli:main'
    },
    'platforms': 'Posix; MacOS X; Windows',
    'include_package_data': False,
    'zip_safe': False,
    'install_requires': ['pyparsing', 'python-magic'],
    'extras_require': {
        'testing': ['pytest']
    }
}


if __name__ == '__main__':
    setup(**META)
