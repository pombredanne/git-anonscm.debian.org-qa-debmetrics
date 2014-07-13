"""This module is a helper for pull_runner and push_runner."""

import os
import os.path
import re
import csv
import datetime
import StringIO
from crontab import CronTab
from debmetrics.models import models
from debmetrics.base import engine, Base, Session

_tables = {}
pkg_dir = os.path.dirname(os.path.abspath(__file__))


def table_factory(name):
    """A factory to generate a class from a table name string.

    Keyword args:
    name -- the table name
    """
    if not name.replace('_', '').isalpha():
        raise ValueError("table name is not valid: %s" % name)
    if name in _tables:
        return _tables[name]

    new_class = models[name]
    _tables[name] = new_class
    return new_class


def table2class(table):
    """Capitalizes the table name to form a class name."""
    return table.title().replace('_', '')


def db_insert(header, rows, table):
    """Inserts data in the database.

    Keyword args:
    header -- the names of the columns
    rows -- the data to be inserted
    table -- the name of the table to insert the data in
    """
    the_class = table_factory(table)
    an_instance = the_class()
    for row in rows:
        for ind, h in enumerate(header):
            setattr(an_instance, h, row[ind])
    try:
        Session.add(an_instance)
        Session.commit()
    except Exception:
        Session.rollback()


def handle_csv(data):
    """Parses csv data and returns the headers and rows.

    Keyword args:
    data -- the csv data
    """
    data = csv.reader(StringIO.StringIO(data))
    rows = []
    rownum = 0
    for row in data:
        if rownum == 0:
            header = row
        else:
            r = []
            for col in row:
                r.append(col)
            rows.append(r)
        rownum += 1
    return header, rows


def should_run(filename, freq):
    """Checks to see if a script should run based on the freq and when it was
    last ran.

    Keyword args:
    filename -- filename of the script to run
    freq -- the crontab string of how frequently to run the script
    """
    job = CronTab(tab=freq + ' dummy')[0]
    if not os.path.exists(os.path.join(pkg_dir, 'last_ran.txt')):
        f = open(os.path.join(pkg_dir, 'last_ran.txt'), 'w')
    with open(os.path.join(pkg_dir, 'last_ran.txt'), 'r') as f:
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
    """Sets the time a script last ran in last_ran.txt.

    Keyword args:
    filename -- the filename of the script
    """
    pat = '.+,' + filename
    now = datetime.datetime.now()
    with open(os.path.join(pkg_dir, 'last_ran.txt'), 'r+') as f:
        if not any(re.search(pat, line) for line in f):
            f.write(date_to_str(now) + ',' + filename + '\n')
            return

    with open(os.path.join(pkg_dir, 'last_ran.txt')) as f:
        out_f = 'last_ran.tmp'
        out = open(out_f, 'w')
        for line in f:
            out.write(re.sub(pat, date_to_str(now) + ',' + filename + '\n',
                      line))
        out.close()
        os.rename(out_f, os.path.join(pkg_dir, 'last_ran.txt'))


def date_to_str(date):
    """Converts a datetime object to a string.

    Keyword args:
    date -- the datetime object
    """
    return datetime.datetime.strftime(date, '%Y-%m-%d %H:%M')


def str_to_date(astring):
    """Converts a string into a datetime object.

    Keyword args:
    astring -- the string
    """
    return datetime.datetime.strptime(astring, '%Y-%m-%d %H:%M')


def db_fetch(table):
    """Fetches data from the database

    Keyword args:
    table -- the table to fetch from
    """
    res = []
    the_class = table_factory(table)
    if hasattr(the_class, 'ts'):
        q = Session.query(the_class).order_by(the_class.ts)
    elif hasattr(the_class, 'an_id'):
        q = Session.query(the_class).order_by(the_class.an_id)
    else:
        q = Session.query(the_class)
    r = q.all()
    for i in r:
        res.append(row2list(i))
    cols = the_class.__table__.columns.keys()
    return res, cols


def pack(data):
    """Packs data into a string of csv to pass with subprocess.

    Keyword args:
    data -- the data to be packed
    """
    return ', '.join(map(str, data))


def row2list(row):
    """Converts a SQLAlchemy row into a list.

    Keyword args:
    row -- a SQLAlchemy row object
    """
    l = []
    for col in row.__table__.columns:
        l.append(str(getattr(row, col.name)))
    return l
