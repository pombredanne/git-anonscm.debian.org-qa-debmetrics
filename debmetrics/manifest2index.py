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
    print """<!doctype html>
<html lang=en>
    <head>
        <meta charset=utf-8>
        <title>Debian Metrics Portal</title>
    </head>
    <body>
        <h1>Debian Metrics Portal</h1>
        <table id="index">
            <tr><th>Metric</th><th>Description</th></tr>"""
    for ind, manifest in enumerate(manifests):
        print '            <tr><td><a href="{{ url_for(\'metric\', metric=\'%s\') }}">%s</a></p></td><td>%s</td></tr>' \
              % (manifest, manifest, descriptions[ind])
    print """       </table>
        <script src="{{ url_for('static2', filename='js/jquery-1.11.1.min.js') }}"></script>
        <script src="{{ url_for('static2', filename='js/jquery.flot.js') }}"></script>
        <script src="{{ url_for('static2', filename='js/jquery.flot.time.js') }}"></script>
        <script src="{{ url_for('static2', filename='js/jquery.flot.hiddengraphs.js') }}"></script>
        <script src="{{ url_for('static2', filename='js/jquery.flot.tooltip.min.js') }}"></script>
        <script> $SCRIPT_ROOT = "";</script>
        <script src="{{ url_for('static2', filename='js/global.js') }}"></script>
    </body>
</html>"""


if __name__ == '__main__':
    sys.argv = sys.argv[1:]
    manifest2index(sys.argv)
