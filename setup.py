from setuptools import setup, find_packages
import os

version = '1.0'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='sixfeetup.karlutils',
      version=version,
      description="Collection of karl utlilities",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='web wsgi karl',
      author='Six Feet Up, Inc.',
      author_email='info@sixfeetup.com',
      url='http://github.com/sixfeetup/sixfeetup.karlutils',
      license='BSD',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['sixfeetup'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'karl'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      sixieutil = sixfeetup.karlutils.scripts.main:main

      [sixfeetup.karlutils.scripts]
      dump_valid_senders = sixfeetup.karlutils.scripts.dump_valid_senders:config_parser
      """,
      )
