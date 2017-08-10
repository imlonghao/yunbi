from setuptools import setup, find_packages
from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='yunbi',
    version='0.2.1',
    keywords=('Yunbi'),
    url='https://github.com/imlonghao/yunbi',
    license='MIT License',
    author='imlonghao',
    author_email='shield@fastmail.com',
    description='A Python wrapper for the yunbi.com api',
    long_description=long_description,
    packages=find_packages(),
    platforms='any'
)
