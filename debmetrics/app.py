#! /usr/bin/python

from flask import Flask, jsonify, request, render_template, send_from_directory
import os
import datetime
app = Flask(__name__)


def get_graph_from_date(t, d):
    for filename in os.listdir('graphs'):
        fileparts = os.path.splitext(filename)[0].split('_')
        if fileparts[0] == t:
            if d in fileparts[-1]:
                return 'graphs/' + filename
    return 'graphs/' + os.listdir('graphs')[0]


def get_graph_name_from_date(t, d):
    for filename in os.listdir('graphs'):
        fileparts = os.path.splitext(filename)[0].split('_')
        if fileparts[0] == t:
            date = fileparts[-1]
            if d in date:
                return date
    return os.path.splitext(os.listdir('graphs'))[0].split('_')[-1]


def get_max_date(t):
    max_date = datetime.datetime.strptime('0010-10-10', '%Y-%m-%d')
    for filename in os.listdir('graphs'):
        fileparts = os.path.splitext(filename)[0].split('_')
        if fileparts[0] == t:
            date = datetime.datetime.strptime(fileparts[-1],
                                              '%Y-%m-%d %H:%M:%S.%f')
            if date > max_date:
                max_date = date
    return max_date.strftime('%Y-%m-%d %H:%M:%S.%f')


def get_min_date(t):
    min_date = datetime.datetime.strptime('9000-10-10', '%Y-%m-%d')
    for filename in os.listdir('graphs'):
        fileparts = os.path.splitext(filename)[0].split('_')
        if fileparts[0] == t:
            date = datetime.datetime.strptime(fileparts[-1],
                                              '%Y-%m-%d %H:%M:%S.%f')
            if date < min_date:
                min_date = date
    return min_date.strftime('%Y-%m-%d %H:%M:%S.%f')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sources')
def sources():
    graphs = []
    names = []
    for filename in os.listdir('graphs'):
        fileparts = os.path.splitext(filename)[0].split('_')
        if fileparts[0] == 'vcs':
            graphs.append('graphs/' + filename)
            names.append(fileparts[-1])
    return render_template('sources.html', graph=graphs[0], name=names[0])


@app.route('/_sources')
def _sources():
    d = request.args.get('d', type=str)
    return jsonify(graph=get_graph_from_date('vcs', d),
                   name=get_graph_name_from_date('vcs', d),
                   maxDate=get_max_date('vcs'),
                   minDate=get_min_date('vcs'))


@app.route('/releases')
def releases():
    return render_template('releases.html')


@app.route('/rc_bugs')
def rc_bugs():
    return render_template('rc_bugs.html')


@app.route('/graphs/<path:filename>')
def graphs(filename):
    return send_from_directory('graphs', filename)


if __name__ == '__main__':
    app.run(debug=True)
