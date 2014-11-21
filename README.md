# Trimming of trailing white spaces.

## Project page
https://github.com/dietmarw/trimtrailingwhitespaces

## About
This script will recursively remove all trailing white spaces in all
text files in a given directory. Binary files and files residing in
version control specific directories are skipped.

As an addition one can also let it clean out obsolete or empty/superfluous
[Modelica](https://modelica.org) *annotations* in  `*.mo` files.

It uses [Adam Hupp](http://hupp.org/adam)'s
[python-magic](https://github.com/ahupp/python-magic) as binary tester.


As a fallback (especially if libmagic is not available, like on Windows)
it acts only on files with a given file extension listed in 'extstring'.

## Releases
You can find the latest stable releases under the
[releases link](../../releases).

## Installation
 * System requirement: Python >= 2.6

Easiest way to install *ttws* is to use [pip](http://www.pip-installer.org).
This will install (and update) *ttws* and also all its depenencies.

### Linux/Mac

    $ sudo pip install -U https://github.com/dietmarw/trimtrailingwhitespaces/archive/v0.5.1.tar.gz

### Windows

    C:\Python27\Scripts>pip.exe install -U https://github.com/dietmarw/trimtrailingwhitespaces/archive/v0.6.0.tar.gz

## Usage:

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
        .mo,.mos,.c,.h,.cpp,.txt,.order

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
            - CRLF = '\r\n' Windows
            - LF = '\n' POSIX
            - CR = '\r' Mac (pre OSX)
            If empty or not specified it is set to the OS default.

        -c, --clean
            WARNING: USE THIS OPTION AT YOUR OWN RISK AS
                     IT *MIGHT* BREAK YOUR CODE!
            Removes obsolete or superfluous annotation constructs
            from Modelica files.
            Only use this if your code is under version control
            and in combination with a careful code-diff review.


## License
See [UNLICENSE](UNLICENSE) file

## Development
 * Author: "Dietmar Winkler" <dietmar.winkler@dwe.no>
 * Contributors: See [graphs/contributors](../../graphs/contributors)

You may report any issues with using the [Issues](../../issues) button.

Contributions in shape of [Pull Requests](../../pulls) are always welcome.
