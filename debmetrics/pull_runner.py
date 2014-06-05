#! /usr/bin/python

import os
import re
import csv
import sys
import logging
import datetime
import subprocess
import ConfigParser
import StringIO
import psycopg2
from crontab import CronTab
from config_reader import settings, read_config

read_config('.debmetrics.ini')
directory = settings['PULL_DIRECTORY']
man_directory = settings['MANIFEST_DIRECTORY']
conn_str = settings['PSYCOPG2_DB_STRING']

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def quote(data):
    if data[0:9] == 'TIMESTAMP':
        return data
    if data.isdigit():
        return data
    return "'" + data + "'"


def db_insert(header, rows, table):
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            rows[i][j] = rows[i][j].replace(',', '')
    try:
        conn = psycopg2.connect(conn_str)
    except Exception:
        logger.error('Unable to connect to database.')
    cur = conn.cursor()
    table_name = 'metrics.%s' % (table)
    for row in rows:
        try:
            cur.execute("INSERT INTO " + table_name + " (%s) VALUES (%s);" %
                        (', '.join(header), ','.join(row)))
        except psycopg2.IntegrityError:
            conn.rollback()
    conn.commit()


def handle_csv(data):
    data = csv.reader(StringIO.StringIO(data))
    rows = []
    rownum = 0
    for row in data:
        if rownum == 0:
            header = row
        else:
            r = []
            for col in row:
                r.append(quote(col))
            rows.append(r)
        rownum += 1
    return header, rows


def should_run(filename, freq):
    job = CronTab(tab=freq + ' dummy')[0]
    if not os.path.exists('last_ran.txt'):
        f = open('last_ran.txt', 'w')
    f = open('last_ran.txt', 'r')
    for line in f:
        line = line.rstrip('\n')
        if line == '':
            continue
        if line.split(',')[1] == filename:
            if str_to_date(line.split(',')[0]) < job.schedule().get_prev():
                update_last_ran(filename)
                return True
            else:
                return False
    # First time ran
    update_last_ran(filename)
    return True


def update_last_ran(filename):
    pat = '.+,' + filename
    now = datetime.datetime.now()
    with open('last_ran.txt', 'r+') as f:
        if not any(re.search(pat, line) for line in f):
                f.write(date_to_str(now) + ',' + filename + '\n')
                return

    with open('last_ran.txt') as f:
        out_f = 'last_ran.tmp'
        out = open(out_f, 'w')
        for line in f:
            out.write(re.sub(pat, date_to_str(now) + ',' + filename + '\n',
                      line))
        out.close()
        os.rename(out_f, 'last_ran.txt')


def date_to_str(date):
    return datetime.datetime.strftime(date, '%Y-%m-%d %H:%M')


def str_to_date(astring):
    return datetime.datetime.strptime(astring, '%Y-%m-%d %H:%M')


def run():
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext == '.py' and not name == '__init__':
            manifest = ConfigParser.RawConfigParser()
            manifest.read(os.path.join(man_directory, name + '.manifest'))
            format = manifest.get('script1', 'format')
            if should_run(name+ext, manifest.get('script1', 'freq')):
                try:
                    output = subprocess.check_output(os.path.join(directory,
                                                                  filename))
                    if format == 'csv':
                        header, rows = handle_csv(output)
                    db_insert(header, rows, name)
                except subprocess.CalledProcessError:
                    logger.error('failure')
            else:
                logger.error('did not run %s', filename)

if __name__ == '__main__':
    run()
