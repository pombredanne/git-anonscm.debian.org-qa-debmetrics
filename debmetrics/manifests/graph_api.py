import matplotlib.pyplot as plt


def pie(x, labels=None, autopct=None):
    plt.pie(x, labels=labels, autopct=autopct)
    plt.legend()
    plt.tight_layout()


def plot(xlabel, ylabel, title, *args, **kwargs):
    plt.plot(*args, **kwargs)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()


def scatter(xlabel, ylabel, title, x, y):
    plt.scatter(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()


def savefig(fname):
    plt.savefig(fname)
