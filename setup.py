
# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = ''

setup(
    long_description=readme,
    name='bwpy',
    version='0.1.8',
    python_requires='==3.*,>=3.7.0',
    author='Rob Wilson',
    author_email='roobert@gmail.com',
    entry_points={"console_scripts": ["bwpy = bwpy.__main__:main"]},
    packages=['bwpy', 'bwpy.bitwarden'],
    package_dir={"": "."},
    package_data={},
    install_requires=['sh==1.*,>=1.12.14'],
    extras_require={"dev": ["black==19.*,>=19.10.0", "toml==0.*,>=0.10.0"]},
)
