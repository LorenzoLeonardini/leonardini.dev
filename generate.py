#!/bin/python

import shutil
import os

shutil.rmtree('build')
os.mkdir('build')

with open('build/index.html', 'w') as f:
    f.write('test 1234')
