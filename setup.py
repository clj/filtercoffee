#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup

setup(name='filtercoffee',
      version='0.3',
      description='A simple WSGI Middleware for compiling CoffeeScript to JavaScript on the fly',
      long_description=open('README', 'r').read(),
      author='Christian Lyder Jacobsen',
      author_email='christian@lyderjacobsen.net',
      url='http://github.com/clj/filtercoffee',
      download_url='https://github.com/downloads/clj/filtercoffee/filtercoffee-0.3.tar.gz',
      py_modules=['filtercoffee'],
      license='BSD',
      classifiers=['Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
                   'License :: OSI Approved :: BSD License',
                   'Intended Audience :: Developers',
                   'Operating System :: OS Independent',
                   'Development Status :: 3 - Alpha',
                   'Programming Language :: JavaScript',
                   'Programming Language :: Python'],
     )

