How to Add a New Metric
***********************
You need the following to add a new metric:

* a manifest
* a script (pull or push)
* a graph script (optional)

Manifest
========
See the manifests directory for example manifests.

Manifest files are parsed by Python's configparser.

The following are the different options available:

type
    pull|push
    
    What kind of metric is it? Pull metric or push metric.

freq
    crontab format
    
    How frequently to call the metric's script.

script
    a filesystem location
    
    The location of the script to be ran on the filesystem.
    Not currently used. Right now the name of the script must
    match the name of the manifest file.

fields
    field1:type1, field2:type2, ...
    
    A comma separated list of fields and the type where the field and type
    are separated by a colon. Used by SQLAlchemy to create the db structure
    and insert and retreive data from the db.

display_fields
    field1, field2, field3, ...
    
    A comma separated list of fields. Use by debmetrics to display on the web
    interface. Unlike fields, the field names do not have to be valid Python
    variables.

format
    csv|json
    
    The format that the script returns data in.

override_ts
    true|false

    If false a ts column is automatically added that stores a timestamp.
    If true the ts column is not added.

delete_before_insert
    true|false

    If true then delete all existing data in the db table before each time new
    data form the script is added to the db. For example, the releases metric
    uses this.

graph_type
    default|custom

    If default, a timeseries graph is generated and displayed. If custom a
    graph script will run that generates a custom graph. It is designed for
    more complex metrics that don't work well with the default timeseries
    graph. Currently there is no way to display custom graphs.

description
    The description is some text that gets displayed to the user. Currently
    the static interface is the only one that displays the description.

token
    Only used by push metrics. Must match the token used in the push script.
    Used to prevent unauthorized pushing of data.

Pull Script
===========

See the debmetrics/pull_scripts directory for example pull scripts.

Your pull script should write data to stdout. For example, if using csv as the
format:

::

    writer = csv.writer(sys.stdout)
    writer.writerow(['field1', 'field2',...]) # replace with actual field names
    writer.writerow([data[0], data[1],...])

Make sure to end your script with exit(0) if everything went okay.

Push Script
===========

The push script goes on a remote server.

It is best to demonstrate push scripts with an example:

::

    #!/usr/bin/python

    import re
    import csv
    import urllib
    import urllib2
    import StringIO
    from BeautifulSoup import BeautifulSoup

    def run():
        url = 'https://bugs.debian.org/release-critical/'
        soup = BeautifulSoup(urllib2.urlopen(url))
        date = soup.findAll('h2')[0]
        p = date.findNext('p')
        nums = re.findall('\d+', p.text)
        url = 'http://metrics.debian.net/push'
        si = StringIO.StringIO()
        cw = csv.writer(si)
        cw.writerow(['ts', 'rc_bugs', 'with_patch', 'with_fix', 'ignored', 'concern_current_stable', 'concern_next_release'])
        cw.writerow([date.text] + nums)
        data = si.getvalue().strip('\r\n')
        values = {'data': data,
                  'metric': 'rc_bug_count',
                  'format': 'csv',
                  'token': '1'}
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        print response.read()

    if __name__ == '__main__':
        run()

The token should match the one in the manifest file.

Graph Script
============

At this time there is no documentation on graph scripts.
