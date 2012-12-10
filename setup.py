# -*- coding: utf-8 -*-

import sys
import os

from setuptools import setup, find_packages

import req

setup(
    name='req',
    version=req.__version__,
    url='https://github.com/dejw/req/',
    license='BSD',
    author='Dawid Fatyga',
    author_email='dawid.fatyga@gmail.com',
    description='req discovers your Python dependencies',
    long_description=req.__doc__,
    py_modules=['req'],
    platforms='any',
    use_2to3=True,
    install_requies=['pip'],
    classifiers=[
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ]
)
