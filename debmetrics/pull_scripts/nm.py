#!/usr/bin/python3

import sys
import csv
import json
import datetime
from urllib.request import urlopen


def run():
    url = 'https://nm.debian.org/public/stats/?json'
    j = json.loads(urlopen(url).read().decode('utf-8'))
    total = 0
    nm = {
            'app_new': 0,
            'app_rcvd': 0,
            'app_hold': 0,
            'adv_rcvd': 0,
            'app_ok': 0,
            'am_rcvd': 0,
            'am': 0,
            'am_hold': 0,
            'am_ok': 0,
            'fd_hold': 0,
            'fd_ok': 0,
            'dam_hold': 0,
            'dam_ok': 0,
            'done': 0,
            'cancelled': 0
        }
    for field in nm.keys():
        nm[field] = j['by_progress'].get(field, 0)
        total = total + nm[field]
    nm['ts'] = '%s' % datetime.datetime.utcnow()
    nm['total'] = total
    writer = csv.DictWriter(sys.stdout, nm.keys())
    writer.writeheader()
    writer.writerow(nm)
    exit(0)


if __name__ == '__main__':
    run()
