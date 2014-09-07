import os
import os.path
import tempfile
import datetime
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors
from matplotlib import dates


def time_series_graph(table, data, cols):
    """Generate a time series graph.

    Keyword args:
    table -- the table the graph is for
    data -- the data to be graphed
    cols -- the column names corresponding to the data
    """
    plt.clf()
    """ None values prevent the graph from generating, so remove any rows with
    them."""
    for row in data:
        if any(x is None for x in row):
            data.remove(row)
    ts, rest = list(zip(*data))[0], list(zip(*data))[1:]
    ts = list(ts)
    for ind, t in enumerate(ts):
        try:
            ts[ind] = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f')
        except Exception:
            ts[ind] = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
    fig = plt.figure()
    sub = fig.add_subplot(111)
    cm = plt.get_cmap('gist_rainbow')
    cNorm  = colors.Normalize(vmin=0, vmax=len(cols)-1)
    scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
    sub.set_color_cycle([scalarMap.to_rgba(i) for i in range(len(cols))])
    fmt = dates.DateFormatter('%Y-%m-%d')
    sub.xaxis.set_major_formatter(fmt)
    count = 0
    for ind, r in enumerate(rest):
        if r[0].isdigit():
            count += 1
            sub.plot(ts, r, label=cols[ind+1])
    plt.title("Time series data for " + table)
    fig.autofmt_xdate()
    legend = sub.legend(loc='top left', bbox_to_anchor=(1.05, 1.0))
    plt.grid(True)
    if not count == 0:
        plt.tight_layout()
        pkg_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(pkg_dir, '..', 'graphs', table + '_timeseries.png')
        plt.savefig(path, bbox_extra_artists=(legend,), bbox_inches='tight')
