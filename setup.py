#!/usr/bin/env python
import os
import logging
import setuptools
from os import path
from importlib import util
from setuptools import setup

logger = logging.getLogger(__name__)

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

spec = util.spec_from_file_location(
    "chinstrap.version", os.path.join("chinstrap", "version.py")
)

# noinspection PyUnresolvedReferences
mod = util.module_from_spec(spec)
spec.loader.exec_module(mod)
version = mod.version

setup(
    install_requires=[
        "requests>=2.27.1",
        "docker>=5.0.3",
        "pytest>=6.2.5",
        "ptpython>=3.0.20",
        "pytezos>=3.3.4",
        "halo>=0.0.31",
        "python-gitlab>=3.1.0",
        "rich>=11.0.0",
        "pre-commit>=2.17.0",
    ],
    license="MIT License",
    name="chinstrap",
    version=version,
    python_requires=">=3.7",
    description="A swiss-army-knife for Tezos Smart Contract developers",
    author="ant4g0nist",
    author_email="me@chinstrap.io",
    url="https://github.com/ant4g0nist/chinstrap",
    scripts=["bin/chinstrap"],
    packages=setuptools.find_packages(),
    package_dir={
        "chinstrap.core.sources.contracts": "chinstrap/core/sources/contracts",
        "chinstrap.core.sources.originations": "chinstrap/core/sources/originations",
        "chinstrap.core.sources.tests": "chinstrap/core/sources/tests",
    },
    package_data={
        "chinstrap.core.sources.contracts": ["*"],
        "chinstrap.core.sources.originations": ["*"],
        "chinstrap.core.sources.tests": ["*"],
        "chinstrap.core.sources": ["*"],
        "chinstrap.core.pytezos.contract": ["*.json"],
    },
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Build Tools",
    ],
)
