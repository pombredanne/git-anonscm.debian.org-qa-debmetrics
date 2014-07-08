#! /usr/bin/python

"""This module contains the Flask code for debmetrics."""

from flask import (Flask, abort, jsonify, request, render_template,
                   send_from_directory)
import os
import datetime
from pull_runner import db_fetch, handle_csv
from push_runner import store, token_matches
from models import models
app = Flask(__name__)


def get_graph_from_date(t, d):
    """Returns the path to a graph.

    Keyword arguments:
    t -- the metric
    d -- the date
    """
    for filename in os.listdir('graphs'):
        fileparts = os.path.splitext(filename)[0].split('_')
        if fileparts[0] == t:
            if d in fileparts[-1]:
                return os.path.join('graphs', filename)
    return os.path.join('graphs', os.listdir('graphs')[0])


def get_graph_name_from_date(t, d):
    """Returns the name corresponding to a graph.

    Keyword arguments:
    t -- the metric
    d -- the date
    """
    for filename in os.listdir('graphs'):
        fileparts = os.path.splitext(filename)[0].split('_')
        if fileparts[0] == t:
            date = fileparts[-1]
            if d in date:
                return date
    return os.path.splitext(os.listdir('graphs')[0])[0].split('_')[-1]


def get_max_date(t):
    """Returns a string representing the most recent date for which a graph
    is available.

    Keyword arguments:
    t -- the metric
    """
    max_date = datetime.datetime.strptime('0010-10-10', '%Y-%m-%d')
    for filename in os.listdir('graphs'):
        fileparts = os.path.splitext(filename)[0].split('_')
        if (fileparts[0] == t and fileparts[-1] != 'timeseries' and
                fileparts[-1] != 'table'):
            date = datetime.datetime.strptime(fileparts[-1],
                                              '%Y-%m-%d %H:%M:%S.%f')
            if date > max_date:
                max_date = date
    return max_date.strftime('%Y-%m-%d %H:%M:%S.%f')


def get_min_date(t):
    """Returns a string representing the oldest date for which a graph
    is available.

    Keyword arguments:
    t -- the metric
    """
    min_date = datetime.datetime.strptime('9000-10-10', '%Y-%m-%d')
    for filename in os.listdir('graphs'):
        fileparts = os.path.splitext(filename)[0].split('_')
        if (fileparts[0] == t and fileparts[-1] != 'timeseries' and
                fileparts[-1] != 'table'):
            date = datetime.datetime.strptime(fileparts[-1],
                                              '%Y-%m-%d %H:%M:%S.%f')
            if date < min_date:
                min_date = date
    return min_date.strftime('%Y-%m-%d %H:%M:%S.%f')


def get_graph_data(t):
    """Returns the data for the dynamic flot graph.

    Keyword arguments:
    t -- the metric
    """
    res, cols = db_fetch(t)
    return res, cols


def get_all_metrics():
    """Returns a list of all metrics."""
    return models.keys()


def graph_helper(t):
    """A helper to retrieve the graphs, corresponding names, and the path to
    the timeseries graph.

    Keyword args:
    t -- the metric
    """
    graphs = []
    timeseries = ''
    names = []
    for filename in os.listdir('graphs'):
        fileparts = os.path.splitext(filename)[0].split('_')
        if '_'.join(fileparts[0:-3]) == t and fileparts[-1] != 'timeseries':
            graphs.append(os.path.join('graphs', filename))
            names.append(fileparts[-1])
        elif '_'.join(fileparts[0:-1]) == t and fileparts[-1] == 'timeseries':
            timeseries = os.path.join('graphs', filename)
    if not graphs:
        graphs.append(None)
    if not names:
        names.append(None)
    return graphs, names, timeseries


@app.route('/')
def index():
    """The index of the website."""
    return render_template('index.html')


@app.route('/<metric>')
def metric(metric):
    """A general route for all metrics. Return 404 if metric does not exist.

    Keyword args:
    metric -- the metric
    """
    if metric in models:
        rows, cols = db_fetch(metric)
        graphs, name, timeseries = graph_helper(metric)
        return render_template('metric.html', title=metric, graph=graphs[0],
                               name=name[0], timeseries=timeseries,
                               headers=cols, rows=rows)
    else:
        abort(404)


@app.route('/_<metric>')
def _sources(metric):
    """A route to get a graph from metric and date.

    Keyword args:
    metric -- the metric
    """
    d = request.args.get('d', type=str)
    return jsonify(graph=get_graph_from_date(metric, d),
                   name=get_graph_name_from_date(metric, d))


@app.route('/_<metric>minmax')
def _sourcesminmax(metric):
    """A route to get the min and max date from metric.

    Keyword args:
    metric -- the metric
    """
    return jsonify(maxDate=get_max_date(metric),
                   minDate=get_min_date(metric))


@app.route('/_<metric>graphdata')
def _metricgraphdata(metric):
    """A route to get the data for the dynamic graph.

    Keyword args:
    metric -- the metric
    """
    res, cols = get_graph_data(metric)
    return jsonify(res=res, cols=cols)


@app.route('/_allmetrics')
def _allmetrics():
    """A route to get a list of all metrics."""
    metrics = get_all_metrics()
    return jsonify(metrics=metrics)


@app.route('/push', methods=['POST'])
def push():
    """A route to push data for a push metric."""
    table = request.form['metric'].encode('utf-8')
    data = request.form['data'].encode('utf-8')
    format = request.form['format'].encode('utf-8')
    token = request.form['token'].encode('utf-8')
    if format == 'csv':
        header, rows = handle_csv(data)
    if token_matches(table, token) and store(table, header, rows):
        return jsonify(result='Success')
    else:
        return jsonify(result='Failure')


@app.route('/graphs/<path:filename>')
def graphs(filename):
    """A route to retrieve a graph from a filename.

    Keyword args:
    filename -- the path to the graph
    """
    return send_from_directory('graphs', filename)


@app.route('/contact')
def contact():
    """A route for contact information."""
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
