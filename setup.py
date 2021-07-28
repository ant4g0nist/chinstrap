#!/usr/bin/env python
import os
import logging
import setuptools
from os import path
from importlib import util
from setuptools import setup
from distutils.errors import DistutilsExecError
from distutils.command.sdist import sdist as sdist_orig

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

logger = logging.getLogger(__name__)
spec = util.spec_from_file_location(
    "chinstrap.version", os.path.join("chinstrap", "version.py")
)

# noinspection PyUnresolvedReferences
mod = util.module_from_spec(spec)
spec.loader.exec_module(mod)  # type: ignore
version = mod.version  # type: ignore

setup(
    install_requires=[
        "docker>=4.4.4",
        "ptpython>=3.0.19",
        "pytezos>=3.2.6",
        "halo>=0.0.31",
        "python-gitlab>=2.10.0",
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
            # smartpy-cli
            'chinstrap.chinstrapCore.smartpyCli': 'chinstrap/chinstrapCore/smartpyCli',
            # resources
            'chinstrap.resources.chinstraps.contracts' : 'chinstrap/resources/chinstraps/contracts',
            'chinstrap.resources.chinstraps.originations' : 'chinstrap/resources/chinstraps/originations',
            'chinstrap.resources.chinstraps.tests' : 'chinstrap/resources/chinstraps/tests'
            },
    package_data = {
                'chinstrap.chinstrapCore.smartpyCli': ['*'] ,
                'chinstrap.resources.chinstraps.contracts' :['*'],
                'chinstrap.resources.chinstraps.originations' :['*'],
                'chinstrap.resources.chinstraps.tests' :['*'],
             },
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Build Tools'
    ]
)