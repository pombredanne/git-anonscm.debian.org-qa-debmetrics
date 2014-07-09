#!/usr/bin/python

"""This modules generates an index file from the manifest file names."""

import sys
import ntpath
import ConfigParser

config = ConfigParser.RawConfigParser()


def manifest2index(manifests):
    """Outputs the index file given a list of manifest files.

    Keyword arguments:
    manifests -- the location of manifests on the filesystem
    """
    descriptions = [0] * len(manifests)
    for ind, manifest in enumerate(manifests):
        config.read(manifest)
        descriptions[ind] = config.get('script1', 'description')
        manifests[ind] = ntpath.basename(manifest).split('.', 1)[0]
    manifests, descriptions = (list(x) for x in zip(*sorted(
                                                    zip(manifests,
                                                        descriptions))))
    print """{% extends "layout.html" %}
    {% block title %}Debmetrics Home {% endblock %}
    {% block body %}
        <h1>Debian Metrics Portal</h1>
        <table id="index">
            <tr><th>Metric</th><th>Description</th></tr>"""
    for ind, manifest in enumerate(manifests):
        print '            <tr><td><a href="{{ url_for(\'metric\', metric=\'%s\') }}">%s</a></p></td><td>%s</td></tr>' \
              % (manifest, manifest, descriptions[ind])
    print """       </table>
    {% endblock %}"""


if __name__ == '__main__':
    sys.argv = sys.argv[1:]
    manifest2index(sys.argv)
