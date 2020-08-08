import setuptools

with open("README.md", "r") as file_obj:
    long_description = file_obj.read()

setuptools.setup(
    name="alacrity",
    version="1.3.4",
    author="Vishnuvardhan Kumar",
    author_email="vishnukumar1997@gmail.com",
    description="Quickstart your Python development with CLI package "
                "templating",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['clint'],
    entry_points={
          'console_scripts': [
              'alacrity = alacrity.core:main'
          ]
      },
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
