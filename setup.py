import setuptools

with open("README.md", "r") as file_obj:
    long_description = file_obj.read()

setuptools.setup(
    name="overlord",
    version="1.0.0",
    author="Vishnuvardhan Kumar",
    author_email="vishnukumar1997@gmail.com",
    description="Quickstarts your Python projects with VC integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[],
    entry_points={
          'console_scripts': [
              'overlord = overlord.main:main'
          ]
      },
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
