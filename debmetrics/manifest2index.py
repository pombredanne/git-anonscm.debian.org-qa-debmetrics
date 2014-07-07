#!/usr/bin/python

"""This modules generates an index file from the manifest file names."""

import sys
import ntpath


def manifest2index(manifests):
    """Outputs the index file given a list of manifest files.

    Keyword arguments:
    manifests -- the location of manifests on the filesystem
    """
    for ind, manifest in enumerate(manifests):
        manifests[ind] = ntpath.basename(manifest).split('.', 1)[0]
    manifests.sort()
    print """<!doctype html>
<html lang=en>
    <head>
        <meta charset=utf-8>
        <title>Debian Metrics Portal</title>
    </head>
    <body>
        <h1>Debian Metrics Portal</h1>"""
    for manifest in manifests:
        print '        <p><a href="{{ url_for(\'metric\', metric=\'%s\') }}">%s</a></p>' \
              % (manifest, manifest)
    print """    </body>
</html>"""


if __name__ == '__main__':
    sys.argv = sys.argv[1:]
    manifest2index(sys.argv)
