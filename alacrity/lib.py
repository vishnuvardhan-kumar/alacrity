from __future__ import print_function
from __future__ import division, absolute_import, unicode_literals

import logging
import os
import shutil
import sys
import subprocess
from clint.textui import colored

string_input = input
if sys.version_info.major == 2:
    string_input = raw_input

is_64bits = sys.maxsize > 2**32

filepath = os.path.abspath(__file__)
dirpath = os.path.dirname(filepath)


def rebuild_persistence(name='persist.ini'):
    """ Rebuild the persist.ini file if missing/corrupted """

    # Default values for persistence
    options = {'invert': False,
               'build': False}

    # Congregated persistence path
    persist_path = os.path.join(dirpath, name)

    # Ensure that persist.ini does not exist
    if os.path.isfile(persist_path):
        print(colored.red("WARN : persist.ini exists, destroy and clean-make (y/n)"))

        choice = string_input()

        if choice == 'y':
            os.remove(persist_path)
        elif choice == 'n':
            print(colored.green("Clean make cancelled, aborting."))
            sys.exit()
        else:
            logging.error(" Invalid choice")

    try:
        with open(persist_path, "w") as file_object:

            # Write main section to ini
            file_object.write('[main]\n')

            for option in options.keys():
                file_object.write('{}={}\n'.format(option, options[option]))
            print(colored.yellow("Persistence was rebuilt successfully."))

    except IOError:
        logging.error("The persist.ini file could not be created.")

    return persist_path, options


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


def create_package_structure(package_name, status):
    """" Creates the initial package structure """

    try:
        os.mkdir(package_name)

        # Create package sub-directory
        sub_directory = '{0}/{0}'.format(package_name)
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

        status['structure_created'] = True

    except IOError:
        logging.error(".py file creation failed at subdirectory.")
    except OSError:
        logging.error("package directory already exists")
        logging.error("Enable clean_make for complete reconstruction")


def create_docs_directory(path, status):
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
        create_makefile('{}/docs'.format(path), status)
        status['docs_created'] = True

    except OSError:
        logging.error("%s/docs directory already exists", path)
        logging.error("Enable clean_make for complete reconstruction")


def create_tests_package(path, status):
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
        status['tests_created'] = True

    except IOError:
        logging.error("py file creation failed at tests directory")
    except OSError:
        logging.error("Enable clean_make for complete reconstruction")


def create_git_ignore(path, status):
    """" Creates a Python .gitignore file in the path"""

    abs_path = os.path.join(dirpath, "starters/gitignore.txt")
    rel_path = os.path.join(dirpath, "gitignore.txt")

    try:
        with open(rel_path, "r") as git_read:
            git_ignore = git_read.read()
    except IOError:
        with open(abs_path, "r") as git_read:
            git_ignore = git_read.read()

    try:
        with open("{}/.gitignore".format(path), "w") as git:
                git.write(git_ignore)
        status['gitignore_created'] = True

    except IOError:
        logging.error(" .gitignore creation failed")


def create_manifest(path, status):
    """" Creates a MANIFEST.in file in the path"""

    abs_path = os.path.join(dirpath, "starters/MANIFEST.in")
    rel_path = os.path.join(dirpath, "MANIFEST.in")

    try:
        with open(rel_path, "r") as man:
            data = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            data = man.read()

    try:
        with open("{}/MANIFEST.in".format(path), "w") as git:
            git.write(data)
        status['manifest_created'] = True

    except IOError:
        logging.error(" MANIFEST.in creation failed")


def create_requirements(path, status):
    """" Creates a requirements.txt file in the path"""

    abs_path = os.path.join(dirpath, "starters/requirements.txt")
    rel_path = os.path.join(dirpath, "requirements.txt")

    try:
        with open(rel_path, "r") as man:
            data = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            data = man.read()

    try:
        with open("{}/requirements.txt".format(path), "w") as git:
            git.write(data)
        status['requirements_created'] = True

    except IOError:
        logging.error(" requirements.txt creation failed")


def create_readme(path, status):
    """" Creates a README.rst file in the path"""

    abs_path = os.path.join(dirpath, "starters/README.rst")
    rel_path = os.path.join(dirpath, "README.rst")

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
        status['readme_created'] = True

    except IOError:
        logging.error(" README.rst creation failed.")


def create_makefile(path, status):
    """" Creates a MAKEFILE in the path"""
    try:
        with open('{}/Makefile'.format(path), 'w') as fobj:
            fobj.close()
        status['makefile_created'] = True

    except IOError:
        logging.error(" Makefile creation failed.")


def create_setup(path, status, test=False):
    """" Create a setup.py file in the path"""

    package_name = path
    version = desc = ""
    author = author_email = ""

    if not test:
        print(colored.green("Enter the initial version:"))
        version = string_input()

        print(colored.green("Enter a brief description:"))
        desc = string_input()

        print(colored.green("Enter author name:"))
        author = string_input()

        print(colored.green("Enter author email:"))
        author_email = string_input()

    abs_path = os.path.join(dirpath, "starters/setup.py")
    rel_path = os.path.join(dirpath, "setup.py")

    try:
        with open(rel_path, "r") as man:
            doc = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            doc = man.read()

    # Make the changes
    if not test:
        doc = doc.replace('[@package_name]', package_name)
        doc = doc.replace('[@version]', version)
        doc = doc.replace('[@desc]', desc)
        doc = doc.replace('[@author]', author)
        doc = doc.replace('[@author_email]', author_email)

    try:
        with open("{}/setup.py".format(path), "w") as wr:
            wr.write(doc)
        status['setup_created'] = True

    except IOError:
        logging.error(" setup.py creation failed.")

    return author


def mit_lic(path, name, year, status):
    """ Create a MIT license """

    abs_path = os.path.join(dirpath, "starters/MIT_LICENSE")
    rel_path = os.path.join(dirpath, "MIT_LICENSE")

    data = read_from_paths(rel_path, abs_path)

    data = data.replace('[@fullname]', name)
    data = data.replace('[@year]', year)

    try:
        with open("{}/LICENSE".format(path), "w") as fobj:
            fobj.write(data)
        status['license_created'] = True

    except IOError:
        logging.error(" LICENSE creation failed.")


def apa_lic(path, name, year, status):
    """ Create an Apache2 license """

    abs_path = os.path.join(dirpath, "starters/APACHE2_LICENSE")
    rel_path = os.path.join(dirpath, "APACHE2_LICENSE")

    data = read_from_paths(rel_path, abs_path)

    data = data.replace('[@fullname]', name)
    data = data.replace('[@year]', year)

    try:
        with open("{}/LICENSE".format(path), "w") as fobj:
            fobj.write(data)
        status['license_created'] = True

    except IOError:
        logging.error(" LICENSE creation failed.")


def gpl_lic(path, status):
    """ Create a GPL license """

    abs_path = os.path.join(dirpath, "starters/GPL_LICENSE")
    rel_path = os.path.join(dirpath, "GPL_LICENSE")

    data = read_from_paths(rel_path, abs_path)

    try:
        with open("{}/LICENSE".format(path), "w") as fobj:
            fobj.write(data)
        status['license_created'] = True

    except IOError:
        logging.error(" LICENSE creation failed.")


def create_license(path, full_name, status):
    """" Prompt user for choice of license and create"""

    print(colored.green("Choose a license: [mit/apache/gpl3]"))
    license_name = string_input()

    fullname = full_name

    print(colored.green("Enter year for license:"))
    year = string_input()

    if license_name == 'mit':
        mit_lic(path, fullname, year, status)
    elif license_name == 'apache':
        apa_lic(path, fullname, year, status)
    elif license_name == 'gpl3':
        gpl_lic(path, status)
    else:
        logging.error(" Invalid license name.")
        logging.info(" Skipping LICENSE creation")


def create_starter_files(path, status):
    """" Create and place various files in the package"""

    # Create standard Python .gitignore
    create_git_ignore(path, status)
    # setup.py
    full_name = create_setup(path, status, test=False)
    # LICENSE
    create_license(path, full_name, status)
    # MANIFEST.in
    create_manifest(path, status)
    # Makefile
    create_makefile(path, status)
    # README.rst
    create_readme(path, status)
    # requirements.txt
    create_requirements(path, status)


def report_status(status):
    """" Reports what processes failed during creation. """

    if not status['structure_created']:
        print(colored.red("WARN : Structure was not created"))
    if not status['gitignore_created']:
        print(colored.red("WARN : .gitignore was not created"))
    if not status['setup_created']:
        print(colored.red("WARN : setup.py was not created"))
    if not status['license_created']:
        print(colored.red("WARN : LICENSE was not created"))
    if not status['manifest_created']:
        print(colored.red("WARN : MANIFEST.in was not created"))
    if not status['makefile_created']:
        print(colored.red("WARN : Makefile was not created"))
    if not status['readme_created']:
        print(colored.red("WARN : README.rst was not created"))
    if not status['requirements_created']:
        print(colored.red("WARN : requirements.txt was not created"))
    if not status['tests_created']:
        print(colored.red("WARN : test directory was not created"))
    if not status['docs_created']:
        print(colored.red("WARN : docs directory was not created"))


def is_git_installed():
    """" Check if git is installed on the system. """

    current_dir = os.getcwd()
    windows_dir = ''

    if sys.platform.startswith('win'):
        # Windows specific code
        if is_64bits:
            windows_dir = os.path.join(os.environ['WINDIR'], 'SysWOW64')
        else:
            windows_dir = os.path.join(os.environ['WINDIR'], 'System32')

        try:
            full_cmd = '{}\\where.exe git'.format(windows_dir)
            cmd_result = subprocess.check_output(full_cmd, cwd=current_dir).strip().decode("utf-8")
            if cmd_result.startswith('INFO'):
                return False
            return cmd_result
        except OSError:
            return False

    elif sys.platform.startswith('linux'):
        # Linux specific code
        try:
            true_cmd_result = subprocess.check_output(['which', 'git'])
            cmd_result = true_cmd_result.decode("utf-8").rstrip()
        except OSError:
            cmd_result = ""

        if 'no git in' in cmd_result or not cmd_result:
            return False

        return cmd_result

    else:
        return False


def git_init(path, status):
    """ Initiates a git repository at the path"""

    git_path = is_git_installed()

    if git_path:
        print(colored.green('Do you want to initialize a Git repository? (y/n)'))
        choice = string_input()

        if choice == 'y':
            command = [git_path, 'init', path]
            value = subprocess.check_output(command).decode("utf-8")
            print(colored.green(value))
        elif choice == 'n':
            print(colored.yellow('Skipping git initialization'))
        else:
            logging.error(" Invalid choice")
            print(colored.yellow('INFO: Skipping git initialization'))

    else:
        print(colored.yellow('INFO: git could not be detected on this machine'))
        print(colored.yellow('INFO: Skipping git initialization'))

if __name__ == '__main__':
    print("Lib.py worked.")
