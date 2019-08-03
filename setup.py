import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="Items Control",
    version="0.1",
    author="Miguel Bolivar",
    author_email="mbol8309@gmail.com",
    description=("Control sell or loan of items in Cuba."),
    license="GNU v3",
    keywords="loan sell control",
    url="http://packages.python.org/an_example_pypi_project",
    packages=['items_control'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
