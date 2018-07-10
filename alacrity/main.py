from __future__ import print_function
from __future__ import division, absolute_import

import logging
import os
from alacrity import lib
import sys

string_input = input
if sys.version_info.major == 2:
    string_input = raw_input


def main():
    """ Starts a new Python package instance"""

    try:
        try:
            print("Enter the name of the package:")
            package_name = string_input()

            # Check for clean_make
            if os.path.isdir(package_name) and os.path.isfile("{0}/{0}/__init__.py".format(package_name)):
                print("The package already exists, destroy and clean make? (y/n)")
                choice = string_input()

                if choice == 'y':
                    lib.remove_package(package_name)
                elif choice == 'n':
                    print("Please pick a different package name, aborting.")
                    sys.exit()
                else:
                    logging.error(" Invalid choice")

            # Create the initial structure
            lib.create_package_structure(package_name)
            # Create starter files
            lib.create_starter_files(package_name)
            # Create docs directory
            lib.create_docs_directory(package_name)
            # Create tests directory
            lib.create_tests_package(package_name)

            print("Package {} was created successfully.".format(package_name))
        except EOFError:
            print("Ctrl+C : Aborting package creation.")
            sys.exit()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
