#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

# This is necessary for nose to handle multiprocessing correctly
from multiprocessing import util  # noqa

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

from packaging.bdist_trinoadmin import bdist_trinoadmin
from release import release

# Import this from util instead of prestoadmin because prestoadmin has third
# party dependencies that can't be resolved by setup.py. Util should not.
from util import __version__

with open('README.rst') as readme_file:
    readme = readme_file.read()

# Requirements for both development and testing are duplicated here
# and in the requirements.txt. Unfortunately this is required by
# tox which relies on the existence of both.

# Note that argparse is special. We don't actually depend on argparse, but
# wheel does. If argparse exists in the system libraries, pip wheel won't
# package it up into the third-party directory, and the resulting dist-offline
# will fail to install if argparse isn't in the system python libraries.
requirements = [
    'pycparser==2.20',
    'argparse==1.4.0',
    'paramiko==2.7.2',
    'Fabric==1.14.1',
    'requests==2.26.0',
    'overrides==2.8.0',
    'pip==20.3.4',
    'setuptools==42.0.2',
    'wheel==0.36.2',
    'flake8==3.9.2',
    'retrying==1.3.3',
    'pyjks==20.0.0',
    'pyjwt==1.7.1'
]

test_requirements = [
    'tox>=2.9.1',
    'nose>=1.3.7',
    'nose-timer>=0.6',
    'mock>=1.0.1',
    'docker-py>=1.5.0',
    'certifi>=2015.4.28',
    'fudge>=1.1.0',
    'PyYAML>=3.11'
]

# =====================================================
# Welcome to HackLand! We monkey patch the _get_rc_file
# method of PyPIRCCommand so that we can read a .pypirc
# that is located in the current directory. This enables
# us to check it in with the code and not require
# developers to create files in their home directory.
from distutils.config import PyPIRCCommand  # noqa


def get_custom_rc_file(self):
    home_pypi = os.path.join(os.path.expanduser('~'),
                             '.pypirc')
    local_pypi = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '.pypirc')
    return local_pypi if os.path.exists(local_pypi) \
        else home_pypi

PyPIRCCommand._get_rc_file = get_custom_rc_file

setup(
    name='trino-admin',
    version=__version__,
    description="Trino-admin installs, configures, and manages Trino/Presto installations.",
    long_description=readme,
    author="wgzhao",
    url='https://github.com/wgzhao/trino-admin',
    packages=find_packages(exclude=['*tests*']),
    package_dir={'trinoadmin':
                 'trinoadmin'},
    package_data={'trinoadmin': ['trino-admin-logging.ini']},
    include_package_data=True,
    install_requires=requirements,
    license="APLv2",
    zip_safe=False,
    keywords='trinoadmin',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'bdist_trinoadmin': bdist_trinoadmin,
              'release': release},
    entry_points={'console_scripts': ['trino-admin = trinoadmin.main:main']}
)
