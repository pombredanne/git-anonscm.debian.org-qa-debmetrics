from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = [l for l in f.read().splitlines()
                        if not l.startswith('#')]

setup(name='debmetrics',
      version='0.0.1',
      install_requires=install_requires,
      description='Debian Metrics Portal for retrieving, updating,' +
      'and display of metrics',
      url='http://anonscm.debian.org/cgit/qa/debmetrics.git/',
      author='Joseph Bisch',
      author_email='joseph.bisch@gmail.com',
      license='AGPL',
      packages=find_packages(),
      )
