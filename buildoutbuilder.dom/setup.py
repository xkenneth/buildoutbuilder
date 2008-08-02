from distutils.core import setup
from setuptools import find_packages

setup(name='buildoutbuilder.dom',
      version='0.1',
      description='Tools for working with buildouts as a DOM',
      author='Kenneth Miller',
      author_email='xkenneth@gmail.com',
      url='buildoutbuilder.googlecode.com',
      namespace_packages = ['buildoutbuilder'],
      packages = find_packages(),
      install_requires = ['setuptools',
                          ]
     )
