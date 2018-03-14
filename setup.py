#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os


def get_locals(filename):
    l = {}
    with open(filename, 'r') as f:
        code = compile(f.read(), filename, 'exec')
        exec(code, {}, l)
    return l


metadata = get_locals(os.path.join('src', 'masterfile', '_metadata.py'))


requirements = [
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='masterfile',
    version=metadata['version'],
    description='Tools for organizing the variables of interest in a study',
    author='Nate Vack',
    author_email='njvack@wisc.edu',
    url='https://github.com/njvack/masterfile',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requirements,
    license='MIT license',
    zip_safe=False,
    keywords='masterfile',
    entry_points={'console_scripts': [
            'make_blank_dictionary = masterfile.scripts.make_blank_dictionary:main',
            'extract_masterfile_data = masterfile.scripts.extract_masterfile_data:main',
            'make_joined_data = masterfile.scripts.make_joined_data:main',
            'text_to_dos = masterfile.scripts.text_to_dos:main',
            'validate_masterfile = masterfile.scripts.validate_masterfile:main',
    ]},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
