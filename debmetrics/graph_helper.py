import os
import tempfile
import datetime
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import dates


def time_series_graph(table, data, cols):
    """Generate a time series graph.

    Keyword args:
    table -- the table the graph is for
    data -- the data to be graphed
    cols -- the column names corresponding to the data
    """
    plt.clf()
    print data
    ts, rest = zip(*data)[0], zip(*data)[1:]
    ts = list(ts)
    for ind, t in enumerate(ts):
        try:
            ts[ind] = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')
        except Exception:
            ts[ind] = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
    fig = plt.figure()
    sub = fig.add_subplot(111)
    fmt = dates.DateFormatter('%Y-%m-%d')
    sub.xaxis.set_major_locator(dates.DayLocator())
    sub.xaxis.set_major_formatter(fmt)
    plt.xticks(rotation=70)
    count = 0
    for ind, r in enumerate(rest):
        if r[0].isdigit():
            count += 1
            sub.plot(ts, r, label=cols[ind+1])
    plt.title("Time series data for " + table)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    if not count == 0:
        plt.savefig(os.path.join('graphs', table + '_timeseries.png'))
