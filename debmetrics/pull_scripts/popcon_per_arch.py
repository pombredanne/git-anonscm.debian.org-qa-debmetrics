#! /usr/bin/python3

import sys
import csv
import calendar
from urllib.request import urlopen
from bs4 import BeautifulSoup


def format_ts(ts):
    ts = ts[4:-4]
    month = ts[0:3]
    months = {v: k for k,v in enumerate(calendar.month_abbr)}
    month = str(months[month])
    if len(month) == 1:
        month = '0' + month
    day = ts[4:6]
    if day[0] == ' ':
        day = '0' + day[1]
    time = ts[7:15]
    year = ts[16:20]
    ts = '%s-%s-%s %s.000000' % (year, month, day, time)
    return ts


def find_between(s, first, last):
    start = s.index(first) + len(first)
    end = s.index(last, start)
    return s[start:end]


def run():
    url = 'http://popcon.debian.org/'
    soup = BeautifulSoup(urlopen(url))
    table = soup.find_all('table')[0]
    td = table.find_all('td')[0]
    footer = soup.find_all('div', {'id': 'footer'})[0]
    ts = find_between(footer.text, 'Last generated on ', '.')
    ts = format_ts(ts)
    columns = ['ts'] + td.text.split()[::4]
    for ind, col in columns:
        columns[ind] = col.replace('-', '_')
    row = [ts] + td.text.split()[2::4]
    writer = csv.writer(sys.stdout)
    writer.writerow(columns)
    writer.writerow(row)
    exit(0)

if __name__ == '__main__':
    run()
