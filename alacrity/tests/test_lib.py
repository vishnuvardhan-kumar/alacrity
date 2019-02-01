# Unittests for the lib.py functions to be placed here

import unittest
import os
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

        lib.create_package_structure(self.test_name, self.status)

        # Verify creation of directories
        self.assertTrue(os.path.isdir(self.test_name))
        self.assertTrue(os.path.isdir(self.sub_directory))

        # Verify creation of files
        self.assertTrue(os.path.isfile(self.initfile))
        self.assertTrue(os.path.isfile(self.corefile))
        self.assertTrue(os.path.isfile(self.libfile))

        # Clean-up the package created
        lib.remove_package(self.test_name)

    def test_create_tests_package(self):
        self.test_name = 'sample_tests_pack'
        self.sub_directory = '{0}/tests'.format(self.test_name)
        self.initfile = '{}/__init__.py'.format(self.sub_directory)
        self.testlibfile = '{}/test_lib.py'.format(self.sub_directory)

        os.mkdir(self.test_name)
        lib.create_tests_package(self.test_name, self.status)

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
        lib.create_git_ignore(self.path, self.status)

        # Check if the file was created successfully
        self.assertTrue(os.path.isfile(self.gitpath))

        lib.remove_package(self.path)

    def test_create_manifest(self):
        self.path = 'test_path'
        self.manpath = '{}/MANIFEST.in'.format(self.path)

        os.mkdir(self.path)
        lib.create_manifest(self.path, self.status)

        # Check if the file was created successfully
        self.assertTrue(os.path.isfile(self.manpath))

        lib.remove_package(self.path)

    def test_create_requirements(self):
        self.path = 'test_path'
        self.reqpath = '{}/requirements.txt'.format(self.path)

        os.mkdir(self.path)
        lib.create_requirements(self.path, self.status)

        # Check if the file was created successfully
        self.assertTrue(os.path.isfile(self.reqpath))

        lib.remove_package(self.path)

    def test_create_readme(self):
        self.path = 'test_path'
        self.readpath = '{}/README.rst'.format(self.path)

        os.mkdir(self.path)
        lib.create_readme(self.path, self.status)

        # Check if the file was created successfully
        self.assertTrue(os.path.isfile(self.readpath))

        lib.remove_package(self.path)

    def test_create_setup(self):
        self.path = "{}/testpath".format(os.path.dirname(__file__))
        self.setuppath = '{}/setup.py'.format(self.path)

        os.mkdir(self.path)
        lib.create_setup(self.path, self.status, test=True)

        # Check if the file was created successfully
        self.assertTrue(os.path.isfile(self.setuppath))

        lib.remove_package(self.path)

    def test_mit(self):
        self.path = "{}/testpath".format(os.path.dirname(__file__))
        self.licpath = '{}/LICENSE'.format(self.path)

        os.mkdir(self.path)
        lib.mit_lic(self.path, 'testname', 'year', self.status)

        # Check if the file was created successfully
        self.assertTrue(os.path.isfile(self.licpath))

        lib.remove_package(self.path)

    def test_apa(self):
        self.path = "{}/testpath".format(os.path.dirname(__file__))
        self.licpath = '{}/LICENSE'.format(self.path)

        os.mkdir(self.path)
        lib.apa_lic(self.path, 'testname', 'year', self.status)

        # Check if the file was created successfully
        self.assertTrue(os.path.isfile(self.licpath))

        lib.remove_package(self.path)

    def test_gpl(self):
        self.path = "{}/testpath".format(os.path.dirname(__file__))
        self.licpath = '{}/LICENSE'.format(self.path)

        lib.remove_package(self.path)
        os.mkdir(self.path)
        lib.gpl_lic(self.path, self.status)

        # Check if the file was created successfully
        self.assertTrue(os.path.isfile(self.licpath))

        lib.remove_package(self.path)

    def test_git_init(self):
        self.path = "{}/testpath".format(os.path.dirname(__file__))

        lib.remove_package(self.path)
        os.mkdir(self.path)

        status = lib.git_init(self.path, self.status, silent=True)

        # Check if the repository was created successfully
        self.assertTrue(status)
        self.assertTrue(os.path.isdir("{}/.git".format(self.path)))

        lib.remove_package(self.path)

    def test_venv_init(self):
        self.path = "{}/testpath".format(os.path.dirname(__file__))

        lib.remove_package(self.path)
        os.mkdir(self.path)

        status = lib.venv_init(self.path, self.status, silent=True)

        # Check if the virtualenv was created successfully
        self.assertTrue(status)
        self.assertTrue(os.path.isdir("{}/testenv".format(self.path)))

        lib.remove_package(self.path)

    def sphinx_init(self):
        self.path = "{}/testpath".format(os.path.dirname(__file__))
        status = lib.sphinx_init(self.path, "testauthor",
                                 "1.0.0", self.status, silent=True)

        # Check if the sphinx dir was created successfully
        self.assertTrue(status)
        self.assertTrue(os.path.isdir("{}/testpath/_build".format(self.path)))
        self.assertTrue(os.path.isdir("{}/testpath/_static".format(self.path)))
        self.assertTrue(
            os.path.isdir("{}/testpath/_templates".format(self.path))
        )

        lib.remove_package(self.path)


if __name__ == '__main__':
    unittest.main()
