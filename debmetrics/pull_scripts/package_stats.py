#!/usr/bin/python3

import sys
import csv
import urllib.request as urllib2


def run():
    url = 'http://ircbots.debian.net/stats/package_differences.txt'
    contents = urllib2.urlopen(url)
    contents = contents.read().decode('utf-8')
    data = csv.reader(contents.splitlines(), delimiter='\t')
    writer = csv.writer(sys.stdout)
    for ind, elem in enumerate(data):
        if ind == 0:
            temp = []
            for e in elem:
                if e == 'timestamp':
                    e = 'ts'
                temp.append(e)
            writer.writerow(temp)
        else:
            if elem[0].startswith('#'):
                continue
            else:
                d = "%s" % elem[0].replace('T', ' ')
                writer.writerow([d, elem[1], elem[2], elem[3], elem[4],
                                 elem[5], elem[6], elem[7], elem[8], elem[9],
                                 elem[10], elem[11], elem[12], elem[13],
                                 elem[14]])
    sys.exit(0)


if __name__ == '__main__':
    run()
