import logging
import os
from os.path import join, isfile, expanduser
from configparser import ConfigParser
import shutil
import sys
import subprocess
import datetime
from clint.textui import colored

filepath = os.path.abspath(__file__)
dirpath = os.path.dirname(filepath)
pythonpath = sys.executable


def rebuild_persistence(name='persist.ini', silent=False):
    """
    Rebuild the persistence of the alacrity subsystem configuration
    :param name: The name of the file storing persistence
    :param silent: Whether to spew information on stdout
    :return: persist_path, options from the configuration
    """

    # Default values for persistence
    options = {'invert': False,
               'build': False}

    # Congregated persistence path
    persist_path = join(dirpath, name)

    # Ensure that persist.ini does not exist
    if os.path.isfile(persist_path):
        print(colored.red("[!] WARN : persist.ini exists, "
                          "destroy and clean-make (y/n) : "), end="")

        choice = input()

        if choice == 'y':
            os.remove(persist_path)
        elif choice == 'n':
            print(colored.green("[*] Clean make persistence cancelled"))
        else:
            logging.error(colored.red(" Invalid choice"))

    try:
        with open(persist_path, "w") as file_object:

            # Write main section to ini
            file_object.write('[main]\n')

            for option in options.keys():
                file_object.write('{}={}\n'.format(option, options[option]))

            if not silent:
                print(colored.yellow("[*] Persistence was rebuilt "
                                     "successfully."))

    except IOError:
        logging.exception(colored.red("[!] The persist.ini file could "
                                      "not be created."))

    return persist_path, options


def read_from_paths(rel_path, abs_path):
    """
    Utility function to read paths (relative and absolute)
    :param rel_path: The relative path of the file
    :param abs_path: The absolute path of the file
    :return: rel_path or abs_path depending on availability and platform
    """

    try:
        with open(rel_path, "r") as man:
            doc = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            doc = man.read()
    return doc


def remove_package(path):
    """
    Remove the package present in path
    :param path: The path to create the git repo at
    :return: None
    """

    try:
        shutil.rmtree(path)
    except OSError:
        logging.exception(colored.red(
            "The path {} could not be removed".format(path)))


def create_package_structure(package_name, status):
    """
    Initialize a package structure in the current directory
    :param package_name: The name of the package (and the directory)
    :param status: Dictionary containing the workflow status
    :return: None
    """

    try:
        os.mkdir(package_name)

        # Create package sub-directory
        sub_directory = '{0}/{0}'.format(package_name)
        os.mkdir(sub_directory)

        # Create __init__.py in subdirectory
        with open(join(sub_directory, "__init__.py"), 'w') as fobj:
            fobj.close()

        # Create core.py in subdirectory
        with open(join(sub_directory, "core.py"), 'w') as fobj:
            fobj.close()

        # Create lib.py in subdirectory
        with open(join(sub_directory, "lib.py"), 'w') as fobj:
            fobj.close()

        status['structure_created'] = True

    except OSError:
        logging.exception(colored.red("package directory already exists"))
        logging.error(colored.red("Enable clean_make for complete "
                                  "reconstruction"))
        logging.error(colored.red(".py file creation failed at subdirectory."))


def create_docs_directory(path, status):
    """
    Create a docs package at path
    :param path: The path to create the docs package at
    :param status: Dictionary containing the workflow status
    :return: None
    """

    try:
        # Create docs directory
        os.mkdir(join(path, "docs"))
        # Create conf.py in docs directory
        with open(join(path, "docs/conf.py"), 'w') as fobj:
            fobj.close()
        with open(join(path, "docs/index.rst"), 'w') as fobj:
            fobj.close()
        with open(join(path, "docs/make.bat"), 'w') as fobj:
            fobj.close()
        create_makefile(join(path, "docs"), status)
        status['docs_created'] = True

    except OSError:
        logging.exception(
            colored.red("%s/docs directory already exists", path)
        )
        logging.error(colored.red("Enable clean_make for complete "
                                  "reconstruction"))


def create_tests_package(path, status):
    """
    Create a tests package at path
    :param path: The path to create the tests package at
    :param status: Dictionary containing the workflow status
    :return: None
    """

    try:
        # Create tests directory
        os.mkdir(join(path, "tests"))
        # Create __init__.py in tests directory
        with open(join(path, "tests/__init__.py"), 'w') as fobj:
            fobj.close()
        # Create test_lib.py in tests directory
        with open(join(path, "tests/test_lib.py"), 'w') as fobj:
            fobj.write("# Place tests for the lib.py functions here. ")
        status['tests_created'] = True

    except IOError:
        logging.exception(colored.red("py file creation failed at "
                                      "tests directory"))
        logging.error(colored.red("Enable clean_make for complete "
                                  "reconstruction"))


def create_git_ignore(path, status):
    """
    Initialize a .gitignore file at path
    :param path: The path to create the gitignore at
    :param status: Dictionary containing the workflow status
    :return: None
    """

    abs_path = join(dirpath, "starters/gitignore.txt")
    rel_path = join(dirpath, "gitignore.txt")

    try:
        with open(rel_path, "r") as git_read:
            git_ignore = git_read.read()
    except IOError:
        with open(abs_path, "r") as git_read:
            git_ignore = git_read.read()

    try:
        with open(join(path, ".gitignore"), "w") as git:
            git.write(git_ignore)
        status['gitignore_created'] = True

    except IOError:
        logging.exception(colored.red(" .gitignore creation failed"))


def create_manifest(path, status):
    """
    Create a manifest at path
    :param path: The path to create the manifest at
    :param status: Dictionary containing the workflow status
    :return: None
    """

    abs_path = join(dirpath, "starters/MANIFEST.in")
    rel_path = join(dirpath, "MANIFEST.in")

    try:
        with open(rel_path, "r") as man:
            data = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            data = man.read()

    try:
        with open(join(path, "MANIFEST.in"), "w") as git:
            git.write(data)
        status['manifest_created'] = True

    except IOError:
        logging.exception(colored.red(" MANIFEST.in creation failed"))


def create_requirements(path, status):
    """
    Create a requirements.txt file at path
    :param path: The path to create the requirements.txt at
    :param status: Dictionary containing the workflow status
    :return: None
    """

    abs_path = join(dirpath, "starters/requirements.txt")
    rel_path = join(dirpath, "requirements.txt")

    try:
        with open(rel_path, "r") as man:
            data = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            data = man.read()

    try:
        with open(join(path, "requirements.txt"), "w") as git:
            git.write(data)
        status['requirements_created'] = True

    except IOError:
        logging.exception(colored.red(" requirements.txt creation failed"))


def create_readme(path, status):
    """
    Create a README.md at path
    :param path: The path to create the README at
    :param status: Dictionary containing the workflow status
    :return: None
    """

    abs_path = join(dirpath, "starters/README.rst")
    rel_path = join(dirpath, "README.rst")

    try:
        with open(rel_path, "r") as man:
            data = man.read()
    except IOError:
        with open(abs_path, "r") as man:
            data = man.read()

    data = data.replace("[@package_name]", path)
    data = data.replace("^$^", "="*len(path), 2)

    try:
        with open(join(path, "README.rst"), "w") as wr:
            wr.write(data)
        status['readme_created'] = True

    except IOError:
        logging.exception(colored.red(" README.rst creation failed."))


def create_makefile(path, status):
    """" Creates a MAKEFILE in the path"""
    try:
        with open(join(path, "Makefile"), 'w') as fobj:
            fobj.close()
        status['makefile_created'] = True

    except IOError:
        logging.exception(colored.red(" Makefile creation failed."))


def create_setup(path, status, test=False):
    """
    Create a setup.py in the package structure in path
    :param path: The path to create the setup at
    :param status: Dictionary containing the workflow status
    :param test: Whether to run in test mode
    :return: None
    """

    package_name = path
    version = desc = ""
    author = author_email = ""

    if not test:
        print(colored.green("[*] Enter the initial version: "), end="")
        version = input()

        print(colored.green("[*] Enter a brief description: "), end="")
        desc = input()

        # Attempt to get author and email from git config
        default_author = ''
        default_email = ''

        gitconfig_path = ''

        # Find git config file
        for i in ['~/.gitconfig', '~/.config/git/config']:
            config_path = expanduser(i)
            if isfile(config_path):
                gitconfig_path = config_path
                break

        if gitconfig_path:
            config = ConfigParser()
            config.read(gitconfig_path)
            if 'user' in config:
                user_section = config['user']
                if 'name' in user_section:
                    default_author = user_section['name']
                if 'email' in user_section:
                    default_email = user_section['email']

        print(
            colored.green(
                "[*] Enter author name [{}]: ".format(default_author)
            ),
            end=""
        )
        author = input() or default_author

        print(
            colored.green(
                "[*] Enter author email [{}]: ".format(default_email)
            ),
            end=""
        )
        author_email = input() or default_email

    abs_path = join(dirpath, "starters/setup.py")
    rel_path = join(dirpath, "setup.py")

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
        with open(join(path, "setup.py"), "w") as wr:
            wr.write(doc)
        status['setup_created'] = True

    except IOError:
        logging.exception(colored.red(" setup.py creation failed."))

    return author, version


def mit_lic(path, name, year, status):
    """
    Write a MIT license at the path
    :param path: The path to create the license at
    :param name: The name of the licensee
    :param year: The year of the license
    :param status: Dictionary containing the workflow status
    :return: None
    """

    abs_path = join(dirpath, "starters/MIT_LICENSE")
    rel_path = join(dirpath, "MIT_LICENSE")

    data = read_from_paths(rel_path, abs_path)

    data = data.replace('[@fullname]', name)
    data = data.replace('[@year]', year)

    try:
        with open(join(path, "LICENSE"), "w") as fobj:
            fobj.write(data)
        status['license_created'] = True

    except IOError:
        logging.exception(colored.red(" LICENSE creation failed."))


def apa_lic(path, name, year, status):
    """
    Write a Apache license at the path
    :param path: The path to create the license at
    :param name: The name of the licensee
    :param year: The year of the license
    :param status: Dictionary containing the workflow status
    :return: None
    """

    abs_path = join(dirpath, "starters/APACHE2_LICENSE")
    rel_path = join(dirpath, "APACHE2_LICENSE")

    data = read_from_paths(rel_path, abs_path)

    data = data.replace('[@fullname]', name)
    data = data.replace('[@year]', year)

    try:
        with open(join(path, "LICENSE"), "w") as fobj:
            fobj.write(data)
        status['license_created'] = True

    except IOError:
        logging.exception(colored.red(" LICENSE creation failed."))


def gpl_lic(path, status):
    """
    Write a GPLv3 license at the path
    :param path: The path to create the license at
    :param status: Dictionary containing the workflow status
    :return: None
    """

    abs_path = join(dirpath, "starters/GPL_LICENSE")
    rel_path = join(dirpath, "GPL_LICENSE")

    data = read_from_paths(rel_path, abs_path)

    try:
        with open(join(path, "LICENSE"), "w") as fobj:
            fobj.write(data)
        status['license_created'] = True

    except IOError:
        logging.exception(colored.red(" LICENSE creation failed."))


def create_license(path, full_name, status):
    """
    Create a license file in the given file
    :param path: The path to create the license at
    :param full_name: The full name of the licensee
    :param status: Dictionary containing the workflow status
    :return: None
    """

    print(colored.green("[*] Choose a license [mit/apache/gpl3]: "), end="")
    license_name = input()
    fullname = full_name
    today = datetime.datetime.today()

    if license_name == 'mit':
        mit_lic(path, fullname, str(today.year), status)
    elif license_name == 'apache':
        apa_lic(path, fullname, str(today.year), status)
    elif license_name == 'gpl3':
        gpl_lic(path, status)
    else:
        print(colored.red("[!] Invalid license name."))
        print(colored.yellow("[>] Skipping license creation"))
        logging.error(colored.red("[!] Invalid license name."))
        logging.info(colored.red("[>] Skipping license creation"))


def create_starter_files(path, status):
    """
    Create and place various starter files in the structure
    :param path: The path to create the starter files at
    :param status: Dictionary containing the workflow status
    :return: author_name, version
    """

    # Create standard Python .gitignore
    create_git_ignore(path, status)
    # setup.py
    full_name, version = create_setup(path, status, test=False)
    # LICENSE
    create_license(path, full_name, status)
    # MANIFEST.in
    create_manifest(path, status)
    # README.rst
    create_readme(path, status)
    # requirements.txt
    create_requirements(path, status)

    return full_name, version


def report_status(status):
    """
    Reports if anything unexpected happened during package creation
    :param status: Dictionary containing the workflow status
    :return: None
    """

    for task in status.keys():
        if not status[task]:
            print(colored.red("[!] WARN : Task {} failed".format(task)))


def git_init(path, status, silent=False):
    """
    Initialize a git repository at path (searches for git in system path)
    :param silent: Whether to run silently with no prompts
    :param path: The path to create the git repo at
    :param status: Dictionary containing the workflow status
    :return: True or False only in silent mode
    """

    git_path = shutil.which('git')

    if silent:
        if git_path is not None:
            command = [git_path, 'init']
            try:
                subprocess.check_output(command, cwd=path).decode('utf-8')
            except subprocess.CalledProcessError:
                return False
            else:
                return True
        else:
            return False

    if git_path:
        print(colored.green('[*] Do you want to initialize a Git repository? '
                            '(y/n) : '), end="")
        choice = input()

        if choice == 'y':
            command = [git_path, 'init', path]
            try:
                subprocess.check_output(command).decode("utf-8")
            except subprocess.CalledProcessError:
                print(colored.red("[!] git initialization subprocess failed, "
                                  "check permissions"))
            else:
                print(colored.green("[*] Initialized empty git repository "
                                    "in {}/.git".format(path)))
        elif choice == 'n':
            print(colored.yellow('[>] Skipping git initialization'))
        else:
            logging.error(colored.red(" Invalid choice"))
            print(colored.red("[!] Invalid choice"))
            print(colored.yellow('[>] Skipping git initialization'))

    else:
        print(colored.yellow('[!] git could not be detected on '
                             'this machine'))
        print(colored.yellow('[>] Skipping git initialization'))

    status['git_initialized'] = True


def venv_init(path, status, silent=False):
    """
    Initialize a virtual environment at path (defaults to venv in Python 3.3+)
    :param path: The path in which the virtualenv will exist
    :param status: Dictionary containing the workflow status
    :param silent: Whether to run the init without any prompts for input
    :return: True or False only in silent mode
    """

    # Check if venv is available
    is_python3_3 = sys.version_info.major == 3 and sys.version_info.minor >= 3

    if is_python3_3:
        command = [pythonpath, '-m', 'venv']
    else:
        logging.error(colored.red("[!] venv could not be detected or "
                                  "executed."))
        print(colored.yellow('[>] Skipping venv initialization'))
        return

    if silent:
        command = [pythonpath, '-m', 'venv', "testenv"]
        try:
            subprocess.check_output(command, cwd=path).decode('utf-8')
        except subprocess.CalledProcessError:
            return False
        else:
            return True

    # Start process
    print(colored.green('[*] Do you want to initialize a virtual environment? '
                        '(y/n): '), end="")
    choice = input()

    if choice == 'y':
        try:
            print(colored.green('[*] Enter a name for the virtual '
                                'environment: '), end="")
            venv_name = input()
            command.append(join(path, venv_name))
            subprocess.check_output(command).decode("utf-8")
        except subprocess.CalledProcessError as e:
            logging.exception(e)
        else:
            print(colored.green("[*] Virtual environment setup complete"))
            status['venv_created'] = True
    elif choice == 'n':
        print(colored.yellow('[>] Skipping virtual environment '
                             'initialization'))
        status['venv_created'] = True
    else:
        logging.error(colored.red(" Invalid choice"))
        print(colored.red("[!] Invalid choice"))
        print(colored.yellow('[>] Skipping venv initialization'))


def sphinx_init(path, author, version, status, silent=False):
    """
    Initialize a Sphinx source dir at path (requires external package Sphinx)
    :param path: The path in which the source dir will exist
    :param author: The name of the author
    :param version: The version of the package
    :param status: Dictionary containing the workflow status
    :param silent: Whether to run without prompts or inputs
    :return: True or False only in silent mode
    """

    is_sphinx = False

    # Check if sphinx is available
    try:
        command = ['sphinx-quickstart', '--version']
        out = subprocess.check_output(command).decode("utf-8")
        if out.startswith('sphinx-quickstart'):
            is_sphinx = True
    except subprocess.CalledProcessError:
        logging.exception(colored.red("[!] Sphinx could not be detected "
                                      "or executed."))
        colored.red("[!] Sphinx could not be detected or executed.")
        print(colored.yellow('[>] Skipping sphinx-docs initialization'))

    if not is_sphinx:
        return

    if silent:
        command = ['sphinx-quickstart', '-q', '-p', path, '-a', author, '-v',
                   version]
        try:
            subprocess.check_output(command).decode('utf-8')
        except subprocess.CalledProcessError:
            return False
        else:
            return True

    # Start process
    print(colored.green('[*] Do you want to initialize Sphinx documentation? '
                        '(y/n): '), end="")
    choice = input()

    if choice == 'y':
        try:
            command = ['sphinx-quickstart', '-q', '-p', path,
                       '-a', author, '-v', version]
            subprocess.check_output(command, cwd=path).decode("utf-8")
        except subprocess.CalledProcessError as e:
            logging.exception(e)
            print(colored.red("[!] Sphinx build failed : {}".format(e)))
        else:
            print(colored.green("[*] Sphinx documentation setup complete"))
            status['sphinx_created'] = True
    elif choice == 'n':
        print(colored.yellow('[>] Skipping Sphinx documentation '
                             'initialization'))
        status['sphinx_created'] = True
    else:
        logging.error(colored.red(" Invalid choice"))
        print(colored.red("[!] Invalid choice"))
        print(colored.yellow('[>] Skipping Sphinx documentation '
                             'initialization'))


if __name__ == '__main__':
    print("Lib.py worked.")
