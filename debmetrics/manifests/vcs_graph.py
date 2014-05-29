#! /usr/bin/python

import datetime
import matplotlib.pyplot as plt


def graph(data):
    for row in data:
        plt.pie([row[5]/float(row[8]), (row[8]-row[5])/float(row[8])])
        plt.savefig('graphs/vcs_vcsusage_pie_' + str(row[0]) + '.png')


if __name__ == '__main__':
    # test data
    graph([
        (datetime.datetime(2014, 5, 1), 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        (datetime.datetime(2014, 5, 2), 11, 12, 13, 14, 15, 16, 17, 18, 19,
            20),
        (datetime.datetime(2014, 5, 3), 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30)])
   
