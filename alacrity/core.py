#!/bin/python

import importlib
import logging
import os
import sys
import argparse
import shutil
from clint.textui import colored

try:
    from alacrity import lib
except ImportError:
    lib = importlib.import_module('lib', '../alacrity')


def main():
    """
    Entry point for the package, alacrity.exe in win and alacrity in linux
    :return: None
    """

    # Start the process
    try:
        from alacrity import version
    except ImportError:
        version = importlib.import_module('version', '../alacrity')

    # Get version information from version.py
    v = version.version()

    parser = argparse.ArgumentParser(description="Alacrity : "
                                                 "Quickstart your Python "
                                                 "package from a terminal")
    parser.add_argument('--make', action='store_true', help="Rebuild "
                                                            "persistence")
    parser.add_argument('--debug', action='store_true', help="Display verbose "
                                                             "debug messages")
    parser.add_argument('--version', action="version", version=v)
    parser.add_argument('package_name')

    args = parser.parse_args()

    if args.make:
        lib.rebuild_persistence()

    if not args.package_name:
        logging.error(" package_name is a required argument")
        sys.exit()

    # Initialize logging depending on debug mode
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    # Initialise status dictionary
    status = {
        'structure_created': False,
        'gitignore_created': False,
        'setup_created': False,
        'license_created': False,
        'manifest_created': False,
        'readme_created': False,
        'requirements_created': False,
        'tests_created': False,
        'git_initialized': False,
        'venv_created': False,
        'sphinx_created': False
    }

    try:
        try:
            package_name = args.package_name

            # Check if the package already exists
            logging.debug("[-] Checking if the package already exists")
            check_is_file = os.path.isfile(
                "{0}/{0}/__init__.py".format(package_name))

            # Check for clean_make
            if os.path.isdir(package_name) or check_is_file:
                logging.debug("[-] Package already exists, "
                              "launching clean make prompt")
                print(colored.red("[!] A package by that name already exists, "
                                  "destroy and clean make? (y/n) : "), end="")
                choice = input()

                logging.debug("[-] Choice prompt input : {}".format(choice))
                if choice == 'y':
                    logging.debug("[-] Removing existing package")
                    lib.remove_package(package_name)
                elif choice == 'n':
                    logging.debug("[-] Clean make cancelled")
                    print(colored.red("[!] Please pick a different package "
                                      "name, aborting."))
                    sys.exit()
                else:
                    logging.error(colored.red(" Invalid choice"))
                    print(colored.red("[!] Invalid choice, aborting"))
                    sys.exit()

            # Create the initial structure
            logging.debug("[-] Creating package structure")
            lib.create_package_structure(package_name, status)
            # Create starter files
            logging.debug("[-] Creating starter files in package")
            author, version = lib.create_starter_files(package_name, status)
            # Create tests directory
            logging.debug("[-] Creating tests package in structure")
            lib.create_tests_package(package_name, status)
            # Initialize git if required and available
            logging.debug("[-] Launching git init submodule")
            lib.git_init(package_name, status)
            # Initialize venv if required and available
            logging.debug("[-] Launching venv init submodule")
            lib.venv_init(package_name, status)
            # Initialize sphinx docs if required and available
            logging.debug("[-] Launching sphinx init submodule")
            lib.sphinx_init(package_name, author, version, status)

            logging.debug("[-] Launching status reporter submodule")
            lib.report_status(status)

            print(colored.green("[|]"))
            print(colored.green("[*] Package {} was created "
                                "successfully.".format(package_name)))
        except EOFError:
            # Catch error thrown by clint.main
            print(colored.yellow("\n[!] Ctrl+C : Aborting package creation."))
            sys.exit()
    except KeyboardInterrupt:
        print(colored.yellow("\n[!] Ctrl+C : Aborting package creation."))

        # Rollback changes
        if os.path.isdir(args.package_name):
            logging.debug("[-] Rolling back committed changes, deleting files")
            shutil.rmtree(args.package_name)

        logging.debug("[-] Alacrity is exiting")
        sys.exit()


if __name__ == '__main__':
    main()
