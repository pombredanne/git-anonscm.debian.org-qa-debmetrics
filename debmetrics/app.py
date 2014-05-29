#! /usr/bin/python

from flask import Flask, jsonify, request, render_template, send_from_directory
import os
app = Flask(__name__)


def get_graph_from_date(t, d):
    for filename in os.listdir('graphs'):
        fileparts = os.path.splitext(filename)[0].split('_')
        if fileparts[0] == 'vcs':
            if d in fileparts[-1]:
                return 'graphs/' + filename
    return 'graphs/' + os.listdir('graphs')[0]


def get_graph_name_from_date(t, d):
    for filename in os.listdir('graphs'):
        fileparts = os.path.splitext(filename)[0].split('_')
        if fileparts[0] == 'vcs':
            date = fileparts[-1]
            if d in date:
                return date
    return os.path.splitext(os.listdir('graphs'))[0].split('_')[-1]


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
                   name=get_graph_name_from_date('vcs', d))


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
