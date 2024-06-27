# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENCE') as f:
    license = f.read()

setup(
    name = 'opencv-security',
    version = '0.0.1',
    description = 'Example for opencv',
    long_description = readme,
    autor = 'Jose Mejia',
    autor_email = 'josmejia.2401@gmail.com',
    url = '',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)