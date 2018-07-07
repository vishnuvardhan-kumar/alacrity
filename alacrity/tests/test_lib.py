# Unittests for the lib.py functions to be placed here

import unittest
from alacrity import lib
import os

filepath = os.path.abspath(__file__)


class TestParser(unittest.TestCase):
    """ Unittests for alacrity/lib.py """

    def test_rebuild_persistence(self):
        # Initialise paths
        self.filepath = filepath
        self.path = '../test_persist.ini'
        self.joinpath = os.path.join(self.filepath, self.path)

        # Test default values
        test_attributes = lib.rebuild_persistence(self.filepath, self.path)
        self.assertEqual(test_attributes['invert'], False)
        self.assertEqual(test_attributes['build'], False)

        # Test creation of file
        self.assertTrue(os.path.isfile(self.joinpath))
        os.remove(self.joinpath)

    def test_read_from_paths(self):
        self.assertTrue(True)

    def test_remove_package(self):
        self.assertTrue(True)

    def test_create_package_structure(self):
        self.assertTrue(True)

    def test_create_docs(self):
        self.assertFalse(False)

    def test_create_tests(self):
        self.assertEqual(2+2, 4)

    def test_create_gitignore(self):
        self.assertTrue(True)

    def test_create_manifest(self):
        self.assertTrue(True)

    def test_create_requirements(self):
        self.assertTrue(True)

    def test_create_readme(self):
        self.assertTrue(True)

    def test_create_makefile(self):
        self.assertTrue(True)

    def test_create_setup(self):
        self.assertTrue(True)

    def test_mit(self):
        self.assertTrue(True)

    def test_apa(self):
        self.assertTrue(True)

    def test_gpl(self):
        self.assertTrue(True)

    def test_create_license(self):
        self.assertTrue(True)

    def test_create_starter_files(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
