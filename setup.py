# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:20:20 2019

@author: wanda
"""

from setuptools import setup, find_packages


setup(
      name='cophelper',
      version='1.0',
      description='A relationship investigation app',
      author='Weilu Wang',
      author_email='wandawwl@gmail.com',
      url='https://github.com/luluww/copHelper',
      packages=find_packages(),
      install_requires=["matplotlib>=3","networkx>=2"],
      license="MIT"      
      )