# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_text = f.read()

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
