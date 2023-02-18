#!/usr/bin/env python
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import os
import shutil
import sys
from distutils import log

from setuptools import find_packages, setup
from setuptools.command.install import install

# obtain version of SoS
with open('src/sos_bash/_version.py') as version:
    for line in version:
        if line.startswith('__version__'):
            __version__ = eval(line.split('=')[1])
            break

setup(
    name="sos-bash",
    version=__version__,
    description='batch execusion actions and bash kernel extension for sos',
    author='Bo Peng',
    url='https://github.com/vatlab/SOS',
    author_email='bpeng@mdanderson.org',
    maintainer='Bo Peng',
    maintainer_email='bpeng@mdanderson.org',
    license='3-clause BSD',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'sos>=0.19.0',
        'sos-notebook>=0.24.0',
    ],
    entry_points='''
[sos_languages]
Bash = sos_bash.kernel:sos_Bash
Zsh = sos_bash.kernel:sos_Bash
''')
