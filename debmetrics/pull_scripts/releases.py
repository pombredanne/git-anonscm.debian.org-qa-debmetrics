#! /usr/bin/python

import sys
import csv


def run():
    data = [
        ['2013-05-04', 'wheezy', '2013-05-04', '7.0'],
        ['2011-02-06', 'squeeze', '2011-02-06', '6.0'],
        ['2009-02-14', 'lenny', '2009-02-14', '5.0'],
        ['2007-04-08', 'etch', '2007-04-08', '4.0'],
        ['2005-06-06', 'sarge', '2005-06-06', '3.1'],
        ['2002-07-19', 'woody', '2002-07-19', '3.0'],
        ['2000-08-15', 'potato', '2000-08-15', '2.2'],
        ['1999-03-09', 'slink', '1999-03-09', '2.1'],
        ['1998-07-24', 'hamm', '1998-07-24', '2.0'],
        ['1997-07-02', 'bo', '1997-07-02', '1.3'],
        ['1996-12-12', 'rex', '1996-12-12', '1.2'],
        ['1996-06-17', 'buzz', '1996-06-17', '1.1']
        ]
    writer = csv.writer(sys.stdout)
    writer.writerow(['ts', 'name', 'release_date', 'release_version'])
    for row in data:
        writer.writerow(row)
    sys.exit(0)

if __name__ == '__main__':
    run()