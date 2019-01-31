#!/bin/python

import importlib
import logging
import os
import sys
import argparse
import shutil
from clint.textui import colored

lib = importlib.import_module('lib', 'alacrity')
version = importlib.import_module('version', 'alacrity')


def main():
    """
    Entry point for the package, alacrity.exe in win and alacrity in linux
    :return: None
    """

    # Get version information from version.py
    v = version.version()

    parser = argparse.ArgumentParser(description="Alacrity : "
                                                 "Quickstart your Python "
                                                 "package from a terminal")
    parser.add_argument('--make', action='store_true', help="Rebuild "
                                                            "persistence")
    parser.add_argument('--version', action="version", version=v)
    parser.add_argument('package_name')

    args = parser.parse_args()

    if args.make:
        lib.rebuild_persistence()

    if not args.package_name:
        logging.error(" package_name is a required argument")
        sys.exit()

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
        'git_initialized': False,
        'venv_created': False
    }

    try:
        try:
            package_name = args.package_name
            check_is_file = os.path.isfile("{0}/{0}/__init__.py".format(package_name))

            # Check for clean_make
            if os.path.isdir(package_name) or check_is_file:
                print(colored.red("A package by that name already exists, "
                                  "destroy and clean make? (y/n)"))
                choice = input()

                if choice == 'y':
                    lib.remove_package(package_name)
                elif choice == 'n':
                    print(colored.red("Please pick a different package name, "
                                      "aborting."))
                    sys.exit()
                else:
                    logging.error(" Invalid choice")
                    sys.exit()

            # Create the initial structure
            lib.create_package_structure(package_name, status)
            # Create starter files
            lib.create_starter_files(package_name, status)
            # Create docs directory
            lib.create_docs_directory(package_name, status)
            # Create tests directory
            lib.create_tests_package(package_name, status)
            # Initialize git if required and available
            lib.git_init(package_name, status)
            # Initialize venv if required and available
            lib.venv_init(package_name, status)

            lib.report_status(status)

            print(colored.yellow("Package {} was created "
                                 "successfully.".format(package_name)))
        except EOFError:
            # Catch error thrown by clint.main
            print(colored.yellow("Ctrl+C : Aborting package creation."))
            sys.exit()
    except KeyboardInterrupt:
        print(colored.yellow("Ctrl+C : Aborting package creation."))

        # Rollback changes
        if os.path.isdir(args.package_name):
            shutil.rmtree(args.package_name)

        sys.exit()


if __name__ == '__main__':
    main()
