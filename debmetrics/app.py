#! /usr/bin/python3

"""This module contains the Flask code for debmetrics."""

from flask import (Flask, abort, jsonify, make_response, request,
                   render_template, send_from_directory, flash, redirect,
                   url_for, g)
from flask_login import (LoginManager, login_user, logout_user,
                             current_user, login_required)
from sqlalchemy.inspection import inspect
import os
import csv
import datetime
import logging
import configparser
import statistics
import io
import json
import operator
from debmetrics.graph_helper import time_series_graph
from debmetrics.runner_helper import min_x, max_x, get_description, get_source, db_list, db_insert, table2class
from debmetrics.pull_runner import db_fetch, handle_csv
from debmetrics.push_runner import store, token_matches
from debmetrics.models import models
from debmetrics.config_reader import settings, read_config
from debmetrics.database import db
from debmetrics.models.user import User

pkg_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=os.path.join(pkg_dir, '..', 'static'), template_folder=os.path.join(pkg_dir, '..', 'templates'))
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.before_request
def before_request():
    g.user = current_user

read_config()

app.config['SECRET_KEY'] = settings['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = settings['DB_URI']
db.init_app(app)

man_dir = settings['MANIFEST_DIRECTORY']
graph_dir = settings['GRAPH_DIRECTORY']
if not os.path.isabs(man_dir):
    man_dir = os.path.join(pkg_dir, man_dir)
if not os.path.isabs(graph_dir):
    graph_dir = os.path.join(pkg_dir, graph_dir)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

os.makedirs(graph_dir, exist_ok=True)


def get_graph_from_date(t, d):
    """Returns the path to a graph.

    Keyword arguments:
    t -- the metric
    d -- the date
    """
    for filename in os.listdir(graph_dir):
        fileparts = os.path.splitext(filename)[0].split('_')
        if fileparts[0] == t:
            if d in fileparts[-1]:
                return os.path.join(graph_dir, filename)
    return os.path.join(graph_dir, os.listdir(graph_dir)[0])


def get_graph_name_from_date(t, d):
    """Returns the name corresponding to a graph.

    Keyword arguments:
    t -- the metric
    d -- the date
    """
    for filename in os.listdir(graph_dir):
        fileparts = os.path.splitext(filename)[0].split('_')
        if fileparts[0] == t:
            date = fileparts[-1]
            if d in date:
                return date
    return os.path.splitext(os.listdir(graph_dir)[0])[0].split('_')[-1]


def get_max_date(t):
    """Returns a string representing the most recent date for which a graph
    is available.

    Keyword arguments:
    t -- the metric
    """
    max_date = datetime.datetime.strptime('0010-10-10', '%Y-%m-%d')
    for filename in os.listdir(graph_dir):
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
    for filename in os.listdir(graph_dir):
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
    res, cols, _, _ = db_fetch(t)
    return res, cols


def get_all_metrics():
    """Returns a list of all metrics."""
    return sorted(models.keys())


def get_metrics_non_ts():
    """Returns a list of non-timeseries metrics."""
    config = configparser.RawConfigParser()
    metrics = []
    for key in models.keys():
        logger.error(key)
        config.read(os.path.join(man_dir, key + '.manifest'))
        override_ts = config.getboolean('script1', 'override_ts')
        if override_ts:
            metrics.append(key)
    return metrics


def get_descriptions():
    """Returns a list of descriptions of metrics."""
    models_list = sorted(models.keys())
    descriptions = []
    for model in  models_list:
        descriptions.append(get_description(model))
    return descriptions


def get_statistics(rows):
    """Returns statistics based on rows.

    Keyword arguments:
    rows -- the data
    """
    stats = {
            'mean': [],
            'sd': [],
            'min': [],
            'max': []
            }
    for col in zip(*rows):
        col = list(col)
        for ind, elem in enumerate(col[:]):
            try:
                col[ind] = int(elem)
            except Exception:
                pass
        for elem in col[:]:
            if not isinstance(elem, int):
                col.remove(elem)
        stats['mean'].append(float(sum(col))/len(col) if len(col) > 0 else 'nan')
        try:
            stats['sd'].append(statistics.stdev(col))
        except Exception:
            stats['sd'].append('nan')
        try:
            stats['min'].append(min(col))
        except Exception:
            stats['min'].append('nan')
        try:
            stats['max'].append(max(col))
        except Exception:
            stats['max'].append('nan')
    return stats


def get_csv(cols, rows):
    """Returns csv data from columns and rows.

    Keyword arguments:
    cols -- the columns
    rows -- the actual data
    """
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(cols)
    for row in rows:
        cw.writerow(row)
    return si.getvalue().strip('\r\n')


def graph_helper(t):
    """A helper to retrieve the graphs, corresponding names, and the path to
    the timeseries graph.

    Keyword args:
    t -- the metric
    """
    graphs = []
    timeseries = ''
    names = []
    for filename in os.listdir(graph_dir):
        fileparts = os.path.splitext(filename)[0].split('_')
        if '_'.join(fileparts[0:-3]) == t and fileparts[-1] != 'timeseries':
            graphs.append(os.path.join('/', graph_dir, filename))
            names.append(fileparts[-1])
        elif '_'.join(fileparts[0:-1]) == t and fileparts[-1] == 'timeseries':
            timeseries = os.path.join('/', graphs_dir, filename)
    if not graphs:
        graphs.append(None)
    if not names:
        names.append(None)
    return graphs, names, timeseries


@app.route('/')
def index():
    """The index of the website."""
    return render_template('index.html')


@app.route('/m/<metric>')
@app.route('/m/<metric>/<desc>')
@app.route('/m/<metric>/<int:page>')
@app.route('/m/<metric>/<desc>/<int:page>')
def metric(metric, desc=None, page=1):
    """A general route for all metrics. Return 404 if metric does not exist.

    Keyword args:
    metric -- the metric
    """
    if metric in models:
        rows, cols, query, the_class = db_fetch(metric)
        statistics = get_statistics(rows)
        try:
            graphs, name, timeseries = graph_helper(metric)
        except Exception as e:
            print('Couldn\'t load graphs. Did you setup the cronjobs?')
            raise e
        source = get_source(metric)
        if desc:
            query = query.order_by(the_class.__dict__[cols[0]].desc())
        paged_rows = query.paginate(page, 20, False)
        mapper = inspect(the_class)
        column_names = list(map(lambda x: str(x)[len(table2class(metric))+1:], mapper.attrs))
        return render_template('metric.html', title=metric, graph=graphs[0],
                               name=name[0], timeseries=timeseries,
                               headers=cols, rows=paged_rows, statistics=statistics,
                               source=source, column_names=column_names, desc=desc)
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
    """A route to get a list of all metrics and descriptions."""
    metrics = get_all_metrics()
    non_ts_metrics = list(metrics)
    for metric in get_metrics_non_ts():
        non_ts_metrics.remove(metric)
    descriptions = get_descriptions()
    return jsonify(non_ts_metrics=list(non_ts_metrics), metrics=list(metrics),
                   descriptions=descriptions)


@app.route('/_<metric>gettable')
def _metricgettable(metric):
    """A route to get the table headers and rows."""
    rows, headers, _, _ = db_fetch(metric)
    return jsonify(headers=headers, rows=rows)


@app.route('/_<metric>getstatistics')
def _metricgetstatistics(metric):
    """A route to get the statistics for a metric."""
    rows, headers, _, _ = db_fetch(metric)
    stats = get_statistics(rows)
    return jsonify(mean=stats['mean'], sd=stats['sd'], min=stats['min'],
                   max=stats['max'], headers=headers)


@app.route('/_axes')
def _axes():
    """A route to get the common xaxis range between multiple metrics."""
    metrics = json.loads(request.args.get('metrics'))
    for ind, metric in enumerate(metrics):
        if ind == 0:
            min_date = min_x(metric)
            max_date = max_x(metric)
        else:
            try:
                if min_x(metric).date() \
                        > min_date.date():
                    min_date = min_x(metric)
            except Exception:
                if min_x(metric).date() \
                        > min_date.date():
                    min_date = min_x(metric)
            try:
                if max_x(metric).date() \
                        < max_date.date():
                    max_date = man_x(metric)
            except Exception:
                if max_x(metric).date() \
                        < max_date.date():
                    max_date = man_x(metric)
    min_date = datetime.datetime.strftime(min_date, '%Y-%m-%d')
    max_date = datetime.datetime.strftime(max_date, '%Y-%m-%d')
    return jsonify(minDate=min_date, maxDate=max_date)


@app.route('/push', methods=['POST'])
def push():
    """A route to push data for a push metric."""
    table = request.form['metric']
    data = request.form['data']
    format = request.form['format']
    token = request.form['token']
    if format == 'csv':
        header, rows = handle_csv(data)
    if token_matches(table, token) and store(table, header, rows):
        rows, cols, _, _ = db_fetch(table)
        time_series_graph(table, rows, cols)
        return jsonify(result='Success')
    else:
        return jsonify(result='Failure')


@app.route('/csv/<metric>')
def csv_route(metric):
    """A route to return csv data for a metric.

    Keyword arguments:
    metric -- a metric
    """
    rows, cols, _, _ = db_fetch(metric)
    csv = get_csv(cols, rows)
    response = make_response(csv)
    response.headers['Content-Disposition'] = \
        'attachment; filename=%s.csv' % (metric,)
    response.headers['Content-Type'] = 'text/csv'
    return response


@app.route('/graphs/<path:filename>')
def graphs(filename):
    """A route to retrieve a graph from a filename.

    Keyword args:
    filename -- the path to the graph
    """
    return send_from_directory(graph_dir, filename)


@app.route('/dynamic')
def dynamic():
    """A route to render the dynamic interface."""
    return render_template('dynamic.html')


@app.route('/thanks')
def thanks():
    """A route for thanking contributors."""
    return render_template('thanks.html')


@app.route('/contact')
def contact():
    """A route for contact information."""
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        flash('Username or password is invalid.', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully.')
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    """A route representing the main admin page."""
    if g.user.username != 'admin':
        flash('Only admin can access admin routes.', 'error')
        return redirect(url_for('index'))
    tables = db_list()
    return render_template('admin.html', tables=tables)


@app.route('/admin/submit_admin_csv_import', methods=['POST'])
@login_required
def submit_admin_csv_import():
    """A route to handle submitting of csv data to be imported into a table"""
    if g.user.username != 'admin':
        flash('Only admin can access admin routes.', 'error')
        return redirect(url_for('admin'))
    table = request.form['table']
    csv = request.form['csv']
    header, rows = handle_csv(csv)
    db_insert(header, rows, table)
    flash('Data was inserted in table %s.' % table)
    return redirect(url_for('admin'))


@app.route('/when_was/<metric>')
def when_was(metric):
    """A route to find when a column was a certain value"""
    ops = {'>': operator.gt, '>=': operator.ge, '<': operator.lt, '<=': operator.le}
    _, _, query, the_class = db_fetch(metric)
    column = request.args.get('column')
    comparison = request.args.get('comparison')
    value = request.args.get('value')
    results = query.filter(ops[comparison](the_class.__dict__[column], value))
    mapper = inspect(the_class)
    column_names = list(map(lambda x: str(x)[len(metric+'.'):], mapper.attrs))
    if comparison[0] == '>':
        results = results.first()
    elif comparison[0] == '<':
        results = results.order_by(the_class.__dict__[column_names[0]].desc()).first()
    return render_template('when_was.html', metric=metric, results=results,
                           column_names=column_names, column=column,
                           comparison=comparison, value=value)


if __name__ == '__main__':
    app.run(debug=True)
