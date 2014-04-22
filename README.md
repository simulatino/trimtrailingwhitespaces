# Trimming of trailing white spaces.

## Project page
https://github.com/dietmarw/trimtrailingwhitespaces

## About
This script will recursively remove all trailing white spaces in all
text files in a given directory. Binary files and files residing in
version control specific directories are skipped.

As an addition one can also let it clean out obsolete or empty/superfluous
Modelica /annotations/ from [Modelica](https://modelica.org) (`*.mo`) files.

It uses a binary tester based on the python magic implementation from
Adam Hupp(http://hupp.org/adam/hg/python-magic)

As a fallback (especially if libmagic is not available, like on Windows)
it acts only on files with a given file extension listed in 'extstring'.

## Releases
You can find the latest stable releases under the
[releases link](../../releases).

## Usage:

    Usage: ttws [OPTIONS] <directory> [<directory> ...]

    This script will recursively remove all trailing white spaces in all
    text files in a given list directories. Binary files and files residing in
    '.bzr', '.cvs', '.git', '.hg', '.svn' directories are skipped.

    Note for Windows users:
    If you do not have libmagic installed, the script will fall back to
    only trim files with the following extensions: .mo,.mos,.c,.h,.cpp,.txt

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


## License
See [UNLICENSE] file

## Development
 * Author: "Dietmar Winkler" <dietmar.winkler@dwe.no>
 * Contributors: See [graphs/contributors](../../graphs/contributors)

You may report any issues with using the [Issues](../../issues) button.

Contributions in shape of [Pull Requests](../../pulls) are always welcome.
