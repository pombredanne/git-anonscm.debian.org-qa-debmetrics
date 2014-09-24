#! /usr/bin/python3

import sys
import csv
import time
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup


def run():
    url = 'http://sources.debian.net/stats/'
    soup = BeautifulSoup(urlopen(url))
    rows = soup.find_all('a', {'name': 'size_cur_releases'})[0]. \
        parent.find_next('table').find_all('tr')
    rownum = 0
    data = []
    for row in rows:
        colnum = 0
        if rownum == 0:
            # header
            thnum = 0
            for th in row.find_all('th'):
                if thnum == 0:
                    # blank th
                    pass
                else:
                    if not len(data) >= thnum:
                        data.append([])
                    data[thnum-1].append(th.find('a').string.strip())
                thnum += 1
        else:
            for col in row.find_all('td'):
                if not len(data) >= colnum + 1:
                    data.append([])
                data[colnum].append(col.string)
                colnum += 1
        rownum += 1
    writer = csv.writer(sys.stdout)
    writer.writerow(['ts', 'disk_usage', 'sloc', 'source_packages',
                     'source_files', 'ctags'])
    for row in data:
        if row[0] == 'wheezy':
            del row[0]
            today = "%s" % datetime.datetime.utcnow()
            row = [today] + row
            writer.writerow(row)
    exit(0)

if __name__ == '__main__':
    run()
