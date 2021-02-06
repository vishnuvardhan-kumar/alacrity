# Unittests for the lib.py functions to be placed here

import unittest
import os
from os.path import join, isdir, isfile
import logging

from alacrity import lib


class TestParser(unittest.TestCase):
    """ Unittests for alacrity.lib """

    def setUp(self):
        self.status = {
            'test_structure_created': False,
            'test_gitignore_created': False,
            'test_setup_created': False,
            'test_license_created': False,
            'test_manifest_created': False,
            'test_readme_created': False,
            'test_requirements_created': False,
            'test_tests_created': False,
            'test_git_initialized': False,
            'test_venv_created': False,
            'test_sphinx_created': False
        }
        logging.basicConfig(level=logging.CRITICAL)

    def test_rebuild_persistence(self):
        # Initialise paths
        self.path = 'test_persist.ini'

        # Test default values
        self.persist, test_attributes = lib.rebuild_persistence(self.path,
                                                                silent=True)
        self.assertEqual(test_attributes['invert'], False)
        self.assertEqual(test_attributes['build'], False)

        # Test creation of file
        self.assertTrue(isfile(self.persist))
        os.remove(self.persist)

    def test_read_from_paths(self):
        self.test_path = 'test_file'
        self.abs_path = os.path.abspath('test_file')

        with open(self.test_path, 'w') as obj:
            obj.write("#Testdata#")

        self.data = lib.read_from_paths(self.test_path, self.abs_path)
        self.assertEqual(self.data, "#Testdata#")
        os.remove(self.test_path)

    def test_remove_package(self):
        self.test_path = 'test_dir'
        os.mkdir(self.test_path)
        lib.remove_package(self.test_path)

        self.assertFalse(isdir(self.test_path))

    def test_create_package_structure(self):
        self.test_name = 'sample_package'
        self.sub_directory = '{0}/{0}'.format(self.test_name)
        self.initfile = join(self.sub_directory, "__init__.py")
        self.corefile = join(self.sub_directory, "core.py")
        self.libfile = join(self.sub_directory, "lib.py")

        lib.create_package_structure(self.test_name, self.status)

        # Verify creation of directories
        self.assertTrue(isdir(self.test_name))
        self.assertTrue(isdir(self.sub_directory))

        # Verify creation of files
        self.assertTrue(isfile(self.initfile))
        self.assertTrue(isfile(self.corefile))
        self.assertTrue(isfile(self.libfile))

        # Clean-up the package created
        lib.remove_package(self.test_name)

    def test_create_tests_package(self):
        self.test_name = 'sample_tests_pack'
        self.sub_directory = '{0}/tests'.format(self.test_name)
        self.initfile = join(self.sub_directory, "__init__.py")
        self.testlibfile = join(self.sub_directory, "test_lib.py")

        os.mkdir(self.test_name)
        lib.create_tests_package(self.test_name, self.status)

        # Verify creation of directories
        self.assertTrue(isdir(self.test_name))
        self.assertTrue(isdir(self.sub_directory))

        # Verify creation of files
        self.assertTrue(isfile(self.initfile))
        self.assertTrue(isfile(self.testlibfile))

        lib.remove_package(self.test_name)

    def test_create_gitignore(self):
        self.path = 'test_path'
        self.gitpath = join(self.path, ".gitignore")

        os.mkdir(self.path)
        lib.create_git_ignore(self.path, self.status)

        # Check if the file was created successfully
        self.assertTrue(isfile(self.gitpath))

        lib.remove_package(self.path)

    def test_create_manifest(self):
        self.path = 'test_path'
        self.manpath = join(self.path, "MANIFEST.in")

        os.mkdir(self.path)
        lib.create_manifest(self.path, self.status)

        # Check if the file was created successfully
        self.assertTrue(isfile(self.manpath))

        lib.remove_package(self.path)

    def test_create_requirements(self):
        self.path = 'test_path'
        self.reqpath = join(self.path, "requirements.txt")

        os.mkdir(self.path)
        lib.create_requirements(self.path, self.status)

        # Check if the file was created successfully
        self.assertTrue(isfile(self.reqpath))

        lib.remove_package(self.path)

    def test_create_readme(self):
        self.path = 'test_path'
        self.readpath = join(self.path, "README.rst")

        os.mkdir(self.path)
        lib.create_readme(self.path, self.status)

        # Check if the file was created successfully
        self.assertTrue(isfile(self.readpath))

        lib.remove_package(self.path)

    def test_create_setup(self):
        self.path = join(os.path.dirname(__file__), "testpath")
        self.setuppath = join(self.path, "setup.py")

        os.mkdir(self.path)
        lib.create_setup(self.path, self.status, test=True)

        # Check if the file was created successfully
        self.assertTrue(isfile(self.setuppath))

        lib.remove_package(self.path)

    def test_mit(self):
        self.path = join(os.path.dirname(__file__), "testpath")
        self.licpath = join(self.path, "LICENSE")

        os.mkdir(self.path)
        lib.mit_lic(self.path, 'testname', 'year', self.status)

        # Check if the file was created successfully
        self.assertTrue(isfile(self.licpath))

        lib.remove_package(self.path)

    def test_apa(self):
        self.path = join(os.path.dirname(__file__), "testpath")
        self.licpath = join(self.path, "LICENSE")

        os.mkdir(self.path)
        lib.apa_lic(self.path, 'testname', 'year', self.status)

        # Check if the file was created successfully
        self.assertTrue(isfile(self.licpath))

        lib.remove_package(self.path)

    def test_gpl(self):
        self.path = join(os.path.dirname(__file__), "testpath")
        self.licpath = join(self.path, "LICENSE")

        lib.remove_package(self.path)
        os.mkdir(self.path)
        lib.gpl_lic(self.path, self.status)

        # Check if the file was created successfully
        self.assertTrue(isfile(self.licpath))

        lib.remove_package(self.path)

    def test_git_init(self):
        self.path = join(os.path.dirname(__file__), "testpath")

        lib.remove_package(self.path)
        os.mkdir(self.path)

        status = lib.git_init(self.path, self.status, silent=True)

        # Check if the repository was created successfully
        self.assertTrue(status)
        self.assertTrue(isdir(join(self.path, ".git")))

        lib.remove_package(self.path)

    def test_venv_init(self):
        self.path = join(os.path.dirname(__file__), "testpath")

        lib.remove_package(self.path)
        os.mkdir(self.path)

        status = lib.venv_init(self.path, self.status, silent=True)

        # Check if the virtualenv was created successfully
        self.assertTrue(status)
        self.assertTrue(isdir(join(self.path, "testenv")))

        lib.remove_package(self.path)

    def sphinx_init(self):
        self.path = join(os.path.dirname(__file__), "testpath")
        status = lib.sphinx_init(self.path, "testauthor",
                                 "1.0.0", self.status, silent=True)

        # Check if the sphinx dir was created successfully
        self.assertTrue(status)
        self.assertTrue(isdir(join(self.path, "testpath/_build")))
        self.assertTrue(isdir(join(self.path, "testpath/_static")))
        self.assertTrue(
            isdir(join(self.path, "testpath/_templates"))
        )

        lib.remove_package(self.path)


if __name__ == '__main__':
    unittest.main()
