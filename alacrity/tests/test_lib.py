# Unittests for the lib.py functions to be placed here

import unittest
from alacrity import lib
import os


class TestParser(unittest.TestCase):
    """ Unittests for alacrity/lib.py """

    def test_rebuild_persistence(self):
        # Initialise paths
        self.path = 'test_persist.ini'

        # Test default values
        self.persist, test_attributes = lib.rebuild_persistence(self.path)
        self.assertEqual(test_attributes['invert'], False)
        self.assertEqual(test_attributes['build'], False)

        # Test creation of file
        self.assertTrue(os.path.isfile(self.persist))
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

        self.assertFalse(os.path.isdir(self.test_path))

    def test_create_package_structure(self):
        self.test_name = 'sample_package'
        self.sub_directory = '{0}/{0}'.format(self.test_name)
        self.initfile = '{}/__init__.py'.format(self.sub_directory)
        self.corefile = '{}/core.py'.format(self.sub_directory)
        self.libfile = '{}/lib.py'.format(self.sub_directory)

        lib.create_package_structure(self.test_name)

        # Verify creation of directories
        self.assertTrue(os.path.isdir(self.test_name))
        self.assertTrue(os.path.isdir(self.sub_directory))

        # Verify creation of files
        self.assertTrue(os.path.isfile(self.initfile))
        self.assertTrue(os.path.isfile(self.corefile))
        self.assertTrue(os.path.isfile(self.libfile))

        # Clean-up the package created
        lib.remove_package(self.test_name)

    def test_create_docs_directory(self):
        self.test_name = 'sample_directory'
        self.sub_directory = '{0}/docs'.format(self.test_name)
        self.conffile = '{}/conf.py'.format(self.sub_directory)
        self.indexfile = '{}/index.rst'.format(self.sub_directory)
        self.makefile = '{}/make.bat'.format(self.sub_directory)

        os.mkdir(self.test_name)
        lib.create_docs_directory(self.test_name)

        # Verify creation of directories
        self.assertTrue(os.path.isdir(self.test_name))
        self.assertTrue(os.path.isdir(self.sub_directory))

        # Verify creation of files
        self.assertTrue(os.path.isfile(self.conffile))
        self.assertTrue(os.path.isfile(self.indexfile))
        self.assertTrue(os.path.isfile(self.makefile))

        lib.remove_package(self.test_name)

    def test_create_tests_package(self):
        self.test_name = 'sample_tests_pack'
        self.sub_directory = '{0}/tests'.format(self.test_name)
        self.initfile = '{}/__init__.py'.format(self.sub_directory)
        self.testlibfile = '{}/test_lib.py'.format(self.sub_directory)

        os.mkdir(self.test_name)
        lib.create_tests_package(self.test_name)

        # Verify creation of directories
        self.assertTrue(os.path.isdir(self.test_name))
        self.assertTrue(os.path.isdir(self.sub_directory))

        # Verify creation of files
        self.assertTrue(os.path.isfile(self.initfile))
        self.assertTrue(os.path.isfile(self.testlibfile))

        lib.remove_package(self.test_name)

    def test_create_gitignore(self):
        self.path = 'test_path'
        self.gitpath = '{}/.gitignore'.format(self.path)

        os.mkdir(self.path)
        lib.create_git_ignore(self.path)

        # Check if the file was created successfully
        self.assertTrue(os.path.isfile(self.gitpath))

        lib.remove_package(self.path)

    def test_create_manifest(self):
        self.path = 'test_path'
        self.manpath = '{}/MANIFEST.in'.format(self.path)

        os.mkdir(self.path)
        lib.create_manifest(self.path)

        # Check if the file was created successfully
        self.assertTrue(os.path.isfile(self.manpath))

        lib.remove_package(self.path)

    def test_create_requirements(self):
        self.path = 'test_path'
        self.reqpath = '{}/requirements.txt'.format(self.path)

        os.mkdir(self.path)
        lib.create_requirements(self.path)

        # Check if the file was created successfully
        self.assertTrue(os.path.isfile(self.reqpath))

        lib.remove_package(self.path)

    def test_create_readme(self):
        self.path = 'test_path'
        self.readpath = '{}/README.rst'.format(self.path)

        os.mkdir(self.path)
        lib.create_readme(self.path)

        # Check if the file was created successfully
        self.assertTrue(os.path.isfile(self.readpath))

        lib.remove_package(self.path)

    def test_create_makefile(self):
        self.path = "{}/testpath".format(os.path.dirname(__file__))
        self.makepath = '{}/Makefile'.format(self.path)

        os.mkdir(self.path)
        lib.create_makefile(self.path)

        # Check if the file was created successfully
        self.assertTrue(os.path.isfile(self.makepath))

        lib.remove_package(self.path)

    # def test_create_setup(self):
    #     self.assertTrue(True)
    #
    # def test_mit(self):
    #     self.assertTrue(True)
    #
    # def test_apa(self):
    #     self.assertTrue(True)
    #
    # def test_gpl(self):
    #     self.assertTrue(True)
    #
    # def test_create_license(self):
    #     self.assertTrue(True)
    #
    # def test_create_starter_files(self):
    #     self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
