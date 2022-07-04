#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from os.path import dirname, join

from setuptools import setup


def get_version(package):
    init_py = open(os.path.join(package, "__init__.py"), encoding="utf-8").read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


def get_package_data(package):
    walk = [
        (dirpath.replace(package + os.sep, "", 1), filenames)
        for dirpath, dirnames, filenames in os.walk(package)
        if not os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename) for filename in filenames])
    return {package: filepaths}


setup(
    name="django-admin-rangefilter",
    version=get_version("rangefilter"),
    url="https://github.com/silentsokolov/django-admin-rangefilter",
    license="MIT",
    description="django-admin-rangefilter app, add the filter by a custom date range on the admin UI.",
    long_description_content_type="text/x-rst",
    long_description=open(join(dirname(__file__), "README.rst"), encoding="utf-8").read(),
    author="Dmitriy Sokolov",
    author_email="silentsokolov@gmail.com",
    packages=get_packages("rangefilter"),
    package_data=get_package_data("rangefilter"),
    include_package_data=True,
    install_requires=[],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    zip_safe=False,
    platforms="any",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
)
