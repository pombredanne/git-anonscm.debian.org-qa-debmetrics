#! /usr/bin/python

import os
import subprocess

for filename in os.listdir('manifests'):
    name, ext = os.path.splitext(filename)
    if ext == '.py' and not name == '__init__':
        if not subprocess.call('./manifests/'+filename, shell=False):
            print 'success'
        else:
            print 'failure'
