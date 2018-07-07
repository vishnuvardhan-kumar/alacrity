from __future__ import print_function
from __future__ import division, absolute_import
from clint.textui import colored

import logging
import os
import shutil
import sys

string_input = input
if sys.version_info.major == 2:
    string_input = raw_input

filepath = os.path.abspath(__file__)


def rebuild_persistence(name='persist.ini'):
    """ Rebuild the persist.ini file if missing/corrupted """

    # Default values for persistence
    options = {'invert': False,
               'build': False}

    # Congregated persistence path
    persist_path = os.path.join(filepath, name)

    # Ensure that persist.ini does not exist
    if os.path.isfile(persist_path):
        os.remove(persist_path)

    try:
        with open(persist_path, "w") as file_object:

            # Write main section to ini
            file_object.write('[main]\n')

            for option in options.keys():
                file_object.write('{}={}\n'.format(option, options[option]))

    except IOError:
        logging.error("The persist.ini file could not be created.")

    return options


def read_from_paths(rel_path, abs_path):
    """ Utility function to read from multiple paths"""
    try:
        with open(rel_path, "r") as man:
            doc = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            doc = man.read()
    return doc


def remove_package(path):
    """" Clear the Python package in the given path for testing. """
    try:
        shutil.rmtree(path)
    except OSError:
        logging.error("The path %s could not be removed", path)


def create_package_structure(package_name):
    """" Creates the initial package structure """

    try:
        os.mkdir(package_name)

        # Create package sub-directory
        sub_directory = '{}/{}'.format(package_name, package_name)
        os.mkdir(sub_directory)

        # Create __init__.py in subdirectory
        with open('{}/__init__.py'.format(sub_directory), 'w') as fobj:
            fobj.close()

        # Create core.py in subdirectory
        with open('{}/core.py'.format(sub_directory), 'w') as fobj:
            fobj.close()

        # Create lib.py in subdirectory
        with open('{}/lib.py'.format(sub_directory), 'w') as fobj:
            fobj.close()

    except IOError:
        logging.error(".py file creation failed at subdirectory.")
    except OSError:
        logging.error("package directory already exists")
        logging.error("Enable clean_make for complete reconstruction")


def create_docs_directory(path):
    """" Creates a docs directory with some starter files """

    try:
        # Create docs directory
        os.mkdir('{}/docs'.format(path))
        # Create conf.py in docs directory
        with open('{}/docs/conf.py'.format(path), 'w') as fobj:
            fobj.close()
        with open('{}/docs/index.rst'.format(path), 'w') as fobj:
            fobj.close()
        with open('{}/docs/make.bat'.format(path), 'w') as fobj:
            fobj.close()
        create_makefile('{}/docs'.format(path))
    except OSError:
        logging.error("%s/docs directory already exists", path)
        logging.error("Enable clean_make for complete reconstruction")


def create_tests_package(path):
    """" Creates a tests directory with an __init__.py """

    try:
        # Create tests directory
        os.mkdir('{}/tests'.format(path))
        # Create __init__.py in tests directory
        with open('{}/tests/__init__.py'.format(path), 'w') as fobj:
            fobj.close()
        # Create test_lib.py in tests directory
        with open('{}/tests/test_lib.py'.format(path), 'w') as fobj:
            fobj.write("# Place tests for the lib.py functions here. ")

    except IOError:
        logging.error("py file creation failed at tests directory")
    except OSError:
        logging.error("Enable clean_make for complete reconstruction")


def create_git_ignore(path):
    """" Creates a Python .gitignore file in the path"""

    abs_path = os.path.join(filepath, "../starters/gitignore.txt")
    rel_path = os.path.join(filepath, "../gitignore.txt")

    try:
        with open(rel_path, "r") as git_read:
            git_ignore = git_read.read()
    except IOError:
        with open(abs_path, "r") as git_read:
            git_ignore = git_read.read()

    try:
        with open("{}/.gitignore".format(path), "w") as git:
                git.write(git_ignore)
    except IOError:
        logging.error(" .gitignore creation failed")


def create_manifest(path):
    """" Creates a MANIFEST.in file in the path"""

    abs_path = os.path.join(filepath, "../starters/MANIFEST.in")
    rel_path = os.path.join(filepath, "../MANIFEST.in")

    try:
        with open(rel_path, "r") as man:
            data = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            data = man.read()

    try:
        with open("{}/MANIFEST.in".format(path), "w") as git:
            git.write(data)
    except IOError:
        logging.error(" MANIFEST.in creation failed")


def create_requirements(path):
    """" Creates a requirements.txt file in the path"""

    abs_path = os.path.join(filepath, "../starters/requirements.txt")
    rel_path = os.path.join(filepath, "../requirements.txt")

    try:
        with open(rel_path, "r") as man:
            data = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            data = man.read()

    try:
        with open("{}/requirements.txt".format(path), "w") as git:
            git.write(data)
    except IOError:
        logging.error(" requirements.txt creation failed")


def create_readme(path):
    """" Creates a README.rst file in the path"""

    abs_path = os.path.join(filepath, "../starters/README.rst")
    rel_path = os.path.join(filepath, "../README.rst")

    try:
        with open(rel_path, "r") as man:
            data = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            data = man.read()

    data = data.replace("[@package_name]", path)
    data = data.replace("^$^", "="*len(path), 2)

    try:
        with open("{}/README.rst".format(path), "w") as wr:
            wr.write(data)
    except IOError:
        logging.error(" README.rst creation failed.")


def create_makefile(path):
    """" Creates a MAKEFILE in the path"""
    try:
        with open('{}/Makefile'.format(path), 'w') as fobj:
            fobj.close()
    except IOError:
        logging.error(" Makefile creation failed.")


def create_setup(path):
    """" Create a setup.py file in the path"""

    package_name = path

    print(colored.green("Enter the initial version:"))
    version = string_input()

    print(colored.green("Enter a brief description:"))
    desc = string_input()

    print(colored.green("Enter author name:"))
    author = string_input()

    print(colored.green("Enter author email:"))
    author_email = string_input()

    abs_path = os.path.join(filepath, "../starters/setup.py")
    rel_path = os.path.join(filepath, "../setup.py")

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

    try:
        with open("{}/setup.py".format(path), "w") as wr:
            wr.write(doc)
    except IOError:
        logging.error(" setup.py creation failed.")

    return author


def mit_lic(path, name, year):
    """ Create a MIT license """

    abs_path = os.path.join(filepath, "../starters/MIT_LICENSE")
    rel_path = os.path.join(filepath, "../MIT_LICENSE")

    data = read_from_paths(rel_path, abs_path)

    data = data.replace('[@fullname]', name)
    data = data.replace('[@year]', year)

    try:
        with open("{}/LICENSE".format(path), "w") as fobj:
            fobj.write(data)
    except IOError:
        logging.error(" LICENSE creation failed.")


def apa_lic(path, name, year):
    """ Create an Apache2 license """

    abs_path = os.path.join(filepath, "../starters/APACHE2_LICENSE")
    rel_path = os.path.join(filepath, "../APACHE2_LICENSE")

    data = read_from_paths(rel_path, abs_path)

    data = data.replace('[@fullname]', name)
    data = data.replace('[@year]', year)

    try:
        with open("{}/LICENSE".format(path), "w") as fobj:
            fobj.write(data)
    except IOError:
        logging.error(" LICENSE creation failed.")


def gpl_lic(path):
    """ Create a GPL license """

    abs_path = os.path.join(filepath, "../starters/GPL_LICENSE")
    rel_path = os.path.join(filepath, "../GPL_LICENSE")

    data = read_from_paths(rel_path, abs_path)

    try:
        with open("{}/LICENSE".format(path), "w") as fobj:
            fobj.write(data)
    except IOError:
        logging.error(" LICENSE creation failed.")


def create_license(path, full_name):
    """" Prompt user for choice of license and create"""

    print(colored.green("Choose a license: [mit/apache/gpl3]"))
    license_name = string_input()

    fullname = full_name

    print(colored.green("Enter year for license:"))
    year = string_input()

    if license_name == 'mit':
        mit_lic(path, fullname, year)
    elif license_name == 'apache':
        apa_lic(path, fullname, year)
    elif license_name == 'gpl3':
        gpl_lic(path)
    else:
        logging.error(" Invalid license name.")
        logging.info(" Skipping LICENSE creation")


def create_starter_files(path):
    """" Create and place various files in the package"""

    # Create standard Python .gitignore
    create_git_ignore(path)
    # setup.py
    full_name = create_setup(path)
    # LICENSE
    create_license(path, full_name)
    # MANIFEST.in
    create_manifest(path)
    # Makefile
    create_makefile(path)
    # README.rst
    create_readme(path)
    # requirements.txt
    create_requirements(path)

if __name__ == '__main__':
    pass
