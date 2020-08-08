# <div align="center">Alacrity</div>

<div align="center">

[![Release](https://img.shields.io/github/v/release/vishnuvardhan-kumar/alacrity.svg)](https://img.shields.io/github/v/release/vishnuvardhan-kumar/alacrity.svg)
[![Build Status](https://travis-ci.org/vishnuvardhan-kumar/alacrity.svg?branch=master)](https://travis-ci.org/vishnuvardhan-kumar/alacrity)
[![Issues](https://img.shields.io/github/issues/vishnuvardhan-kumar/alacrity.svg)](https://img.shields.io/github/issues/vishnuvardhan-kumar/alacrity.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Stars](https://img.shields.io/github/stars/vishnuvardhan-kumar/alacrity.svg?style=social&label=Star)](https://img.shields.io/github/stars/vishnuvardhan-kumar/alacrity?style=social&label=Star)


Quickstart your Python project with a single handy command.

</div>

![Screenshot](https://raw.githubusercontent.com/vishnuvardhan-kumar/alacrity/master/alacrity/tests/scr.png)

## Installation

`pip install alacrity`

## Running Alacrity

To run alacrity, use:

`alacrity <package_name>`

To display all the options, use:

`alacrity -h`

Answer some questions interactively, and poof, your package structure is ready.
Based on the [sample Python package](https://github.com/kennethreitz/samplemod) structure by Kenneth Reitz.

## Features
 - Customized setup.py file
 - Automatic git repository initialization
 - Automatic virtual environment setup
 - Automatic Sphinx docs initialization
 - Easily extensible workflow for custom install steps 

## Platforms
 - Windows (and Cygwin)
 - Linux
 - Android (Termux)

## Testing
 - To run the built-in tests, run `tox` in the project root
 - To add custom testing, edit `tox.ini`