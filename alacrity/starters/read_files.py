from clint.textui import colored
import sys
import os

string_input = input
if sys.version_info.major == 2:
    string_input = raw_input


def read_from_paths(rel_path, abs_path):
    """ Utility function to read from multiple paths"""
    try:
        with open(rel_path, "r") as man:
            doc = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            doc = man.read()
    return doc


def read_git_ignore(filepath):
    """" Reads Python .gitignore file and returns content"""

    abs_path = os.path.join(filepath, "starters/gitignore.txt")
    rel_path = os.path.join(filepath, "gitignore.txt")

    try:
        with open(rel_path, "r") as git_read:
            git_ignore = git_read.read()
    except IOError:
        with open(abs_path, "r") as git_read:
            git_ignore = git_read.read()

    return git_ignore


def read_manifest():
    """" Reads a MANIFEST.in file and returns content"""

    abs_path = "starters/MANIFEST.in"
    rel_path = "MANIFEST.in"

    try:
        with open(rel_path, "r") as man:
            data = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            data = man.read()

    return data


def read_requirements():
    """" Reads requirements.txt file and returns content"""

    abs_path = "starters/requirements.txt"
    rel_path = "requirements.txt"

    try:
        with open(rel_path, "r") as man:
            data = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            data = man.read()

    return data


def read_readme(path):
    """" Reads README.rst file and returns modified content"""

    abs_path = "starters/README.rst"
    rel_path = "README.rst"
    try:
        with open(rel_path, "r") as man:
            data = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            data = man.read()

    data = data.replace("[@package_name]", path)
    data = data.replace("^$^", "="*len(path), 2)

    return data


def read_setup(path):
    """" Read and modify setup.py file in the path"""

    package_name = path

    print(colored.green("Enter the initial version:"))
    version = string_input()

    print(colored.green("Enter a brief description:"))
    desc = string_input()

    print(colored.green("Enter author name:"))
    author = string_input()

    print(colored.green("Enter author email:"))
    author_email = string_input()

    abs_path = "starters/setup.py"
    rel_path = "setup.py"

    try:
        with open(rel_path, "r") as man:
            doc = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            doc = man.read()

    # Make the changes
    doc = doc.replace('[@package_name]', package_name)
    doc = doc.replace('[@version]', version)
    doc = doc.replace('[@desc]', desc)
    doc = doc.replace('[@author]', author)
    doc = doc.replace('[@author_email]', author_email)

    return doc


def read_mit_lic(name, year):
    """ Read a MIT license """

    abs_path = "starters/MIT_LICENSE"
    rel_path = "MIT_LICENSE"

    data = read_from_paths(rel_path, abs_path)

    data = data.replace('[@fullname]', name)
    data = data.replace('[@year]', year)

    return data


def read_apa_lic(name, year):
    """ Read an Apache2 license """

    abs_path = "starters/APACHE2_LICENSE"
    rel_path = "APACHE2_LICENSE"

    data = read_from_paths(rel_path, abs_path)

    data = data.replace('[@fullname]', name)
    data = data.replace('[@year]', year)

    return data


def read_gpl_lic():
    """ Read a GPL license """

    abs_path = "starters/GPL_LICENSE"
    rel_path = "GPL_LICENSE"

    data = read_from_paths(rel_path, abs_path)

    return data