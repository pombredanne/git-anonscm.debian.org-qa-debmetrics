#! /usr/bin/python

import sys
import csv
import time
import datetime
import urllib2
from BeautifulSoup import BeautifulSoup


def run():
    url = 'http://sources.debian.net/stats/'
    soup = BeautifulSoup(urllib2.urlopen(url))
    rows = soup.findAll('a', {'name': 'size_cur_releases'})[0]. \
        parent.findNext('table').findAll('tr')
    rownum = 0
    data = []
    for row in rows:
        colnum = 0
        if rownum == 0:
            # header
            thnum = 0
            for th in row.findAll('th'):
                if thnum == 0:
                    # blank th
                    pass
                else:
                    if not len(data) >= thnum:
                        data.append([])
                    data[thnum-1].append(th.find('a').string.strip())
                thnum += 1
        else:
            for col in row.findAll('td'):
                if not len(data) >= colnum + 1:
                    data.append([])
                data[colnum].append(col.string)
                colnum += 1
        rownum += 1
    writer = csv.writer(sys.stdout)
    writer.writerow(['ts', 'name', 'disk_usage', 'sloc', 'source_packages',
                     'source_files', 'ctags'])
    for row in data:
        today = "'%s'::timestamp" % datetime.datetime.utcnow()
        row = [today] + row
        writer.writerow(row)
        time.sleep(2)
    sys.exit(0)

if __name__ == '__main__':
    run()
