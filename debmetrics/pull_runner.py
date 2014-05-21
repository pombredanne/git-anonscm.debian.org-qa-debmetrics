import os
import subprocess

for filename in os.listdir('examples/manifests'):
    name, ext = os.path.splitext(filename)
    if ext == '.py' and not name == '__init__':
        if subprocess.call('./examples/manifests/'+filename, shell=True):
            # success
            pass
        else:
            # failure
            pass
