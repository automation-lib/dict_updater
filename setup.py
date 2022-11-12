from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Nested Dict Update With operation like insert , deleter , updater ,search '
LONG_DESCRIPTION = 'Recursive Dict Update with insert , deleter , update option'

# Setting up
setup(
    name="dictupdate",
    version=VERSION,
    author="Chetan",
    author_email="chetankolhe72@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['dict updater', 'json update', 'recursive dict updater', 'recursive json updater', 'dict updater','nested dicts'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    fullname="Chetan Kolhe",
    url="https://github.com/automation-lib/dict_updater"
)