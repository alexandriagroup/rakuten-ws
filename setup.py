#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os.path as op


from codecs import open
from setuptools import setup


def read(fname):
    ''' Return the file content. '''
    here = op.abspath(op.dirname(__file__))
    with open(op.join(here, fname), 'r', 'utf-8') as fd:
        return fd.read()

readme = read('README.rst')
changelog = read('CHANGES.rst').replace('.. :changelog:', '')

requirements = [
    'furl',
    'requests',
    'zeep',
    'xmljson'
]

version = ''
version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                    read(op.join('rakuten_ws', '__init__.py')),
                    re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='rakuten-ws',
    author='Salem Harrache',
    author_email='salem.harrache@abc-culture.fr',
    version=version,
    url='https://github.com/alexandriagroup/rakuten-ws',
    packages=[
        'rakuten_ws',
    ],
    package_dir={'rakuten_ws': 'rakuten_ws'},
    install_requires=requirements,
    include_package_data=True,
    license='MIT license',
    zip_safe=False,
    description='Unofficial Python Client for Rakuten Web Service',
    long_description=readme + '\n\n' + changelog,
    keywords='rakuten-ws',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
