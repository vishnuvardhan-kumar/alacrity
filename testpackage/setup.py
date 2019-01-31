# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('LICENSE') as lic_file:
    license_text = lic_file.read()

setup(
    name="testpackage",
    version="1",
    description="something",
    long_description=readme,
    author="someone",
    author_email="someemail",
    license=license_text,
    packages=find_packages(exclude=('tests', 'docs'))
)
