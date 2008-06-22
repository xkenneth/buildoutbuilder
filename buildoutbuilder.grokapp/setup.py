from setuptools import setup, find_packages

version = '0.0'

setup(name='BuildoutBuilder',
      version=version,
      description="",
      long_description="""\
""",
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[], 
      keywords="",
      author="",
      author_email="",
      url="",
      license="",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages = ['buildoutbuilder'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'grok',
                        'megrok.kss',
                        # Add extra requirements here
                        ],
      entry_points="""
      # Add entry points here
      """,
      )
