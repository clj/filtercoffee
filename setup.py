#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup

setup(name='FilterCoffee',
      version='0.1',
      description='A simple WSGI Middleware for compiling CoffeeScript to JavaScript on the fly',
      #long_description='',
      author='Christian Lyder Jacobsen',
      author_email='christian@lyderjacobsen.org',
      url='http://github.com/clj/filtercoffee',
      py_modules=['filtercoffee'],
      license='BSD',
      classifiers=['Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
                   'License :: OSI Approved :: BSD License',
                   'Intended Audience :: Developers',
                   'Programming Language :: JavaScript',
                   'Programming Language :: Python'],
     )

