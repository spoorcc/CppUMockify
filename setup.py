from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CppUMockify',
    version='0.0.6',
    description='Generate CppUMock implementations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/spoorcc/cppumockify',
    author='spoorcc',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='cpputest cppumock pycparser',

    py_modules=["cppumockify"],
    install_requires=['pycparser'],

    entry_points={
        'console_scripts': [
            'cppumockify=cppumockify.main:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/spoorcc/cppumockify/issues',
        'Source': 'https://github.com/spoorcc/cppumockify/',
    },
)
