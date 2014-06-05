#! /usr/bin/python

import os
import ast
import fileinput
import graph_api


def graph(data):
    for row in data:
        pie_labels = ['using vcs', 'not using vcs']
        graph_api.pie([float(row[5])/float(row[8]),
                      (float(row[8])-float(row[5])) / float(row[8])],
                      labels=pie_labels, autopct='%.1f')
        graph_api.savefig(os.path.join('graphs', 'vcs_vcsusage_pie_' + str(row[0]) + '.png'))


if __name__ == '__main__':
    """ test data
    graph([
        (datetime.datetime(2014, 5, 1), 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        (datetime.datetime(2014, 5, 2), 11, 12, 13, 14, 15, 16, 17, 18, 19,
            20),
        (datetime.datetime(2014, 5, 3), 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30)])
    """
    inp = ''
    for line in fileinput.input():
        inp += line
    inp = ast.literal_eval('[' + inp + ']')
    graph(inp)
