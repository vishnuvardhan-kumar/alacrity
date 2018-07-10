# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('LICENSE') as lic_file:
    license_text = lic_file.read()

setup(
    name="[@package_name]",
    version="[@version]",
    description="[@desc]",
    long_description=readme,
    author="[@author]",
    author_email="[@author_email]",
    license=license_text,
    packages=find_packages(exclude=('tests', 'docs'))
)
