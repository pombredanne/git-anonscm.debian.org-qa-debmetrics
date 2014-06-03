#!/usr/bin/python

import ast
import fileinput
import graph_api


def graph(data):
    pass


if __name__ == '__main__':
    inp = ''
    for line in fileinput.input():
        inp += line
    inp = ast.literal_eval('[' + inp + ']')
    graph(inp)
