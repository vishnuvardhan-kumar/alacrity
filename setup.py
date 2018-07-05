import setuptools

with open("README.md", "r") as file_obj:
    long_description = file_obj.read()

setuptools.setup(
    name="alacrity",
    version="0.1.2",
    author="Vishnuvardhan Kumar",
    author_email="vishnukumar1997@gmail.com",
    description="Quickstart your Python development with CLI package templating",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['clint'],
    entry_points={
          'console_scripts': [
              'alacrity = alacrity.main:main'
          ]
      },
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
