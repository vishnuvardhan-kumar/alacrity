from __future__ import print_function
from __future__ import division, absolute_import

import logging
import os
from alacrity import lib
import sys
from clint.textui import colored

string_input = input
if sys.version_info.major == 2:
    string_input = raw_input


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


def main():
    """ Starts a new Python package instance"""

    # Initialise status dictionary
    status = {
        'structure_created': False,
        'gitignore_created': False,
        'setup_created': False,
        'license_created': False,
        'manifest_created': False,
        'makefile_created': False,
        'readme_created': False,
        'requirements_created': False,
        'tests_created': False,
        'docs_created': False,
    }

    # Add invert handler
    arguments_passed = sys.argv[1:]

    if '--make' in arguments_passed:
        lib.rebuild_persistence()
        sys.exit()

    try:
        try:
            print(colored.green("Enter the name of the package:"))
            package_name = string_input()

            # Check for clean_make
            if os.path.isdir(package_name) or os.path.isfile("{0}/{0}/__init__.py".format(package_name)):
                print(colored.red("A package by that name already exists, destroy and clean make? (y/n)"))
                choice = string_input()

                if choice == 'y':
                    lib.remove_package(package_name)
                elif choice == 'n':
                    print(colored.red("Please pick a different package name, aborting."))
                    sys.exit()
                else:
                    logging.error(" Invalid choice")

            # This structure could be optimized further
            # Create the initial structure
            lib.create_package_structure(package_name, status)
            # Create starter files
            lib.create_starter_files(package_name, status)
            # Create docs directory
            lib.create_docs_directory(package_name, status)
            # Create tests directory
            lib.create_tests_package(package_name, status)

            report_status(status)
            print(colored.yellow("Package {} was created successfully.".format(package_name)))
        except EOFError:
            # Catch error thrown by clint.main
            print(colored.yellow("Ctrl+C : Aborting package creation."))
            sys.exit()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
