#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

settings = dict()

# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Topic :: Internet',
    'Topic :: Utilities',
]

settings.update(
    name='catches',
    version='0.1',
    description='Catches',
    long_description=open('README.rst').read(),
    author='Stefano Dipierro',
    license='Apache 2.0',
    url='https://github.com/dipstef/catches',
    classifiers=CLASSIFIERS,
    keywords='exceptions exception handling',
    packages= ['catches'],
    test_suite='tests',
)

setup(**settings)