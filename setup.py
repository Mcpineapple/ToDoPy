#!/usr/bin/env python

from setuptools import setup
import os


thelibFolder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')
install_requires = []
if os.path.isfile(thelibFolder):
    with open(thelibFolder) as f:
        install_requires = f.read().splitlines()

setup(name="ToDoPy",
      version="1.0",
      description="Task todolist app",
      packages=['ToDoPy'],
      install_requires=install_requires
      )
