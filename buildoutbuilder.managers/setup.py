from distutils.core import setup
from setuptools import find_packages

setup(name='buildoutbuilder.managers',
      version='0.1',
      description='Buildout Builder buildout creation/parsing package.',
      author='Kenneth Miller',
      author_email='xkenneth@gmail.com',
      url='buildoutbuilder.googlecode.com',
      namespace_packages = ['buildoutbuilder'],
      packages = find_packages(),
      install_requires = ['setuptools',
                          ]
     )
