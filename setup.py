# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='robotstxt',
    version='0.1',
    author='IGARASHI Masanao',
    author_email='syoux2@gmail.com',
    url='https://github.com/masayuko/robotstxt/',
    license='MIT',
    description='A robots.txt Manipulation Library for Python',
    long_description=open('README.rst').read(),
    keywords='robots',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['robotstxt'],
    install_requires=['urilib'],
    test_suite='tests'
)
