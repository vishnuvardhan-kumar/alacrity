# alacrity

[![PyPI version](https://badge.fury.io/py/alacrity.svg)](https://badge.fury.io/py/alacrity)
[![Build Status](https://travis-ci.org/vishnuvardhan-kumar/alacrity.svg?branch=master)](https://travis-ci.org/vishnuvardhan-kumar/alacrity)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)


Quickstart your Python project with a single handy command.

`pip install alacrity`

To display all the options and the command syntax, use:

`alacrity -h`

Answer some questions interactively, and poof, your package structure is ready.

Based on the [sample Python package](https://github.com/kennethreitz/samplemod) structure by Kenneth Reitz.

Tested to work on :
 - Windows (and Cygwin)
 - Linux (anything except Android Terminal Emulators)

A sample alacrity flow:
```
(venv) sc4r@fsx> alacrity testpackage
[*] Enter the initial version: 0.1.0
[*] Enter a brief description: This is a test package
[*] Enter author name: Vishnuvardhan S
[*] Enter author email: test@abc.com
[*] Choose a license [mit/apache/gpl3]: mit
[*] Enter year for license: 2019
[*] Do you want to initialize a Git repository? (y/n): y
[*] Initialized empty Git repository in /alacrity-test/venv/.git
[*] Do you want to initialize a virtual environment? (y/n): y
[*] Enter a name for the virtual environment: testenv
[*] Virtual environment setup complete
[|]
[*] Package testpackage was created successfully.

(venv) sc4r@fsx>
```