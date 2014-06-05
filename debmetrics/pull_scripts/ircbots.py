#!/usr/bin/python

import sys
import csv
import urllib2


def run():
    url = 'http://ircbots.debian.net/stats/package_differences.txt'
    contents = urllib2.urlopen(url)
    data = list(csv.reader(contents, delimiter='\t'))
    writer = csv.writer(sys.stdout)
    for ind, elem in enumerate(data):
        if ind == 0:
            continue
        else:
            if elem[0].startswith('#'):
                continue
            else:
                d = "TIMESTAMP '%s'" % elem[0]
                writer.writerow([d, elem[1], elem[2], elem[3], elem[4],
                                 elem[5], elem[6], elem[7], elem[8], elem[9],
                                 elem[10], elem[11], elem[12], elem[13],
                                 elem[14]])
    sys.exit(0)


if __name__ == '__main__':
    run()
