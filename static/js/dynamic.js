function isNumber(obj) {
    return !isNaN(parseFloat(obj));
}

if (!window.jQuery) {
    var messageEl = document.createElement('span');
    messageEl.innerHTML = 'JQuery is not available. If you are the operator of'
	    + ' this server, make sure you have run minified_grabber to'
	    + ' fetch it along with other JavaScript and CSS dependencies not'
	    + ' shipped directly with debmetrics.';
    document.getElementById('content').appendChild(messageEl);
}

var metric = $('h1').text();

if ($('input#date')) {
    $('input#date').bind('change', function() {
        $.getJSON($SCRIPT_ROOT + '/_' + metric, {
            d: $('input#date').val()
        }, function(data) {
            $('#graph').attr('src', data.graph);
            $('.title').each(function() {$(this).text(data.name)});
        });
        return false;
    });
}

if ($('input#date')) {
    $.getJSON($SCRIPT_ROOT + '/_' + metric + 'minmax', {},
            function(data) {
                $('input#date').datepicker('option', 'maxDate', data.maxDate);
                $('input#date').datepicker('option', 'minDate', data.minDate);
            });
}

if (typeof datepicker !== 'undefined' && $.isFunction(datepicker)) {
    $('input#date').datepicker({
        dateFormat: "yy-mm-dd",
    });
}

$('#content').append('<div id="graph-table-container"></div>');
/*$('<div id="tabs" class="cf"><ul><li><a href="#graph-tab">Graph</a>'
       + '</li><li><a href="#table-tab">Table</a></li></ul>'
       + '<div id="graph-tab"></div><div id="table-tab"></div></div>').insertBefore('footer');*/
$('#graph-table-container').append('<div id="flot-graph" style="width: 500px;'
      + ' height: 300px; float: left"></div>');
$('#flot-graph').append('<span id="help-text">Use the dropdown to select a metric. Click on ' +
        'the buttons to add the metric to the graph or show it in the table. Click on "Remove' +
        ' all metrics" to remove the graph and table. Click on the options accordion to modify' +
        ' options relating to the graph.</span>');
$('#graph-table-container').append('<div id="flot-graph-legend" style="float: left"></div>');
var descriptions = [];
$.getJSON($SCRIPT_ROOT + '/_allmetrics', {},
        function(data) {
            descriptions = data.descriptions;
            var select = $('<select></select>').attr('id', 'metrics-list');
            $.each(data.metrics, function(i, el) {
                select.append('<option value="' + el + '">' + el + '</option>');
            });
            var textbox = $('<textarea disabled cols="20", rows="6"></textarea>').attr('id', 'description-textarea').attr('style', 'vertical-align: top');
            select.insertBefore('#add-metric');
            textbox.insertBefore('#add-metric');
            $('#metrics-list').change(function() {
                $('#metrics-list option:selected').each(function() {
                    $('#description-textarea').val(descriptions[$(this).index()]);
                });
            });
            $('#metrics-list').change();
       });
$('#graph-table-container').append('<button id="add-metric">Add metric to graph</button>');
$('#graph-table-container').append('<button id="show-table">Show metric in table</button>');
$('#graph-table-container').append('<button id="remove-metrics">Remove all metrics</button>');
$('#graph-table-container').append('<div id="accordion" style="float: right"><h3>Options</h3><div id="options"><div id="graph-dim-container"' +
       ' style="border: 1px solid black; padding: 8px;' +
       '">Graph dimensions:</div><div id="xaxis-range-container" style="border: 1px solid black; padding: 8px;">' +
       'X-axis range:</div></div></div>')
$('#graph-dim-container').append('<div style="">width:' +
       '<input id="graph-width" value="500" />px</div><br />');
$('#graph-dim-container').append('<div style="">height:' +
       '<input id="graph-height" value="300" />px</div>');
$('#graph-dim-container').append('<button id="resize-graph">Update graph dimensions</button>');
$('#xaxis-range-container').append('<div>start: <input id="xaxis-start" /></div>');
$('#xaxis-range-container').append('<div>end: <input id="xaxis-end" /></div>');
$('#xaxis-range-container').append('<button id="update-xaxis-range">Update x-axis range</button>');
// $('#xaxis-start').datepicker();
// $('#xaxis-end').datepicker();
// $('#xaxis-start').datepicker('setDate', '07/01/2014');

var metrics = [];
var indices = [];
var index = 0;
var lastIndex;
var plot

$('#add-metric').click(function() {
    var metric = $('select#metrics-list').val();
    if ($.inArray(metric, metrics) === -1) {
        metrics.push(metric);
        indices.push(index);
        addToGraph();
        updateAxes();
    }
});

$('#show-table').click(function() {
    displayInTable();
});

$('#remove-metrics').click(removeAllMetrics);

$('#resize-graph').click(resizeGraph);

$('#update-xaxis-range').click(updateXaxisRange);

var d = [];

if (typeof $.plot !== 'undefined' && $.isFunction($.plot)) {
    function addToGraph() {
        var metric = $('select#metrics-list').val();
        $.getJSON($SCRIPT_ROOT + '/_' + metric + 'graphdata', {},
            function(data) {
                var pairs = [];
                var labels = [];
                for (var i=0; i < data.res.length; i++) {
                    var x = Date.parse(data.res[i][0].replace('-', '-').substring(0, data.res[i][0].indexOf(' ')));
                    var ys = data.res[i].slice(1);
                    for (var j=0; j < ys.length; j++) {
                        if (isNumber(ys[j])) {
                            if (i==0) {
                                pairs[j] = [];
                                labels.push(data.cols.slice(1)[j]);
                            }
                            pairs[j].push([x, ys[j]]);
                        }
                    }
                }
                index += labels.length + 1;
                lastIndex = index;
                for (var i=0; i < pairs.length; i++) {
                    d.push({label: labels[i], data: pairs[i]});
                }
                var options = {
                    xaxis: {
                        mode: 'time'
                    },
                    legend: {
                        container: $('#flot-graph-legend'),
                        hideable: true,
                    },
                    grid: {
                        hoverable: true
                    },
                    tooltip: true,
                    tooltipOpts: {
                    },
                    metrics: metrics,
                    indices: indices,
                    lastIndex: lastIndex
                };
                plot = $.plot(('#flot-graph'), d, options);
                var start = $('.flot-x-axis .flot-tick-label').first().text();
                var end = $('.flot-x-axis .flot-tick-label').last().text();
                $('#xaxis-start').datepicker();
                $('#xaxis-end').datepicker();
                $('#xaxis-start').datepicker('setDate', formatDate(start));
                $('#xaxis-end').datepicker('setDate', formatDate(end));
            });
    }
}

function formatDate(date) {
    var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    var components = date.split(' ');
    var res = '0';
    res += ($.inArray(components[0], months) + 1);
    res += '/01/';
    res += components[1];
    return res;
}

function updateIndices(i) {
    for (var j=0; j < indices.length; j++) {
        if (indices[j] >= i) {
            indices[j] = indices[j] - 1;
        }
    }
    plot.getOptions().indices = indices;
    plot.setData(d);
    plot.setupGrid();
    plot.draw();
}

function removeColumnGraph(column) {
    for (var i=0; i < d.length; i++) {
        if (d[i].label === column) {
            d.splice(i, 1);
        }
    }
    ind = $.inArray(column, metrics);
    if (ind !== -1) {
        metrics.splice(ind, 1);
        indices.splice(ind, 1);
    }
    plot.getOptions().metrics = metrics;
    plot.getOptions().indices = indices;
    index -= 1;
    lastIndex = index;
    plot.getOptions().lastIndex = lastIndex;
    plot.setData(d);
    plot.setupGrid();
    plot.draw();
}

function removeAllMetrics() {
    d = [];
    metrics = [];
    indices = [];
    index = 0;
    lastIndex = 0;
    if (typeof plot !== 'undefined') {
        plot.setData(d);
        plot.setupGrid();
        plot.draw();
    }
    $('#table-container').remove();
    $('#table_wrapper').remove();
    $('#csvLink').remove();
}

function displayInTable() {
    var table_metric = $('select#metrics-list').val();
    $.getJSON($SCRIPT_ROOT + '/_' + table_metric + 'gettable', {},
        function(data) {
            $('#table-container').remove();
            $('#table_wrapper').remove();
            $('#csvLink').remove();
            var headers = data.headers;
            var rows = data.rows;
            table = '<div id="table-container" style="clear: both;"><table id="table" class="tablesorter"><thead><tr>'
            for (var i=0; i < headers.length; i++) {
                var header = headers[i];
                table += '<th>' + header + '</th>';
            }
            table += '</tr></thead>';
            for (var i=0; i < rows.length; i++) {
                row = rows[i];
                table += '<tr>';
                for (var j=0; j < row.length; j++) {
                    col = row[j];
                    table += '<td>' + col + '</td>';
                }
                table += '</tr>';
            }
            table += '</table></div>';
            var csvLink = '<a id="csvLink" href="csv/' + table_metric + '">Download ' + table_metric + ' CSV</a>';
            $('#graph-table-container').append(table);
            $('#table-container').prepend(csvLink);
            $('#table').dataTable();
        });
    $.getJSON($SCRIPT_ROOT + '/_' + table_metric + 'getstatistics', {},
        function(data) {
            var mean = data.mean;
            var sd = data.sd;
            var min = data.min;
            var max = data.max;
            var table = '<table class="tablesorter">';
            table += '<tr><th>Statistic</th>';
            for (var i=0; i < data.headers.length; i++) {
                table += '<th>' + data.headers[i] + '</th>';
            }
            table += '</tr>';
            table += '<tr><td>Mean</td>';
            for (var i=0; i < mean.length; i++) {
                if (!isNaN(parseFloat(mean[i])) && String(mean[i]).indexOf('.') !== -1) {
                    table += '<td>' + mean[i].toFixed(3) + '</td>';
                } else {
                    table += '<td>' + mean[i] + '</td>';
                }
            }
            table += '</tr><tr><td>SD</td>';
            for (var i=0; i < sd.length; i++) {
                if (!isNaN(parseFloat(sd[i])) && String(sd[i]).indexOf('.') !== -1) {
                    table += '<td>' + sd[i].toFixed(3) + '</td>';
                } else {
                    table += '<td>' + sd[i] + '</td>';
                }
            }
            table += '</tr><tr><td>Min</td>';
            for (var i=0; i < min.length; i++) {
                if (!isNaN(parseFloat(min[i])) && String(min[i]).indexOf('.') !== -1) {
                    table += '<td>' + min[i].toFixed(3) + '</td>';
                } else {
                    table += '<td>' + min[i] + '</td>';
                }
            }
            table += '</tr><tr><td>Max</td>';
            for (var i=0; i < max.length; i++) {
                if (!isNaN(parseFloat(max[i])) && String(max[i]).indexOf('.') !== -1) {
                    table += '<td>' + max[i].toFixed(3) + '</td>';
                } else {
                    table += '<td>' + max[i] + '</td>';
                }
            }
            table += '</tr></table>';
            $('#table-container').append(table);
        });

}

function resizeGraph() {
    var placeholder = $('#flot-graph');
    var w = $('#graph-width').val();
    var h = $('#graph-height').val();
    if (w != 0 && h != 0) {
        placeholder.width(w).height(h);
        plot.resize();
        plot.setupGrid();
        plot.draw();
    }
}

function updateXaxisRange() {
    var start = $('#xaxis-start').val();
    var end = $('#xaxis-end').val();
    start = Date.parse(start);
    end = Date.parse(end);
    plot.getOptions().xaxes[0].min = start;
    plot.getOptions().xaxes[0].max = end;
    plot.setupGrid();
    plot.draw();
}

function updateAxes() {
    $.getJSON($SCRIPT_ROOT + '/_axes', {metrics: JSON.stringify(metrics)},
            function(data) {
                plot.getOptions().xaxes[0].min = Date.parse(data.minDate);
                plot.getOptions().xaxes[0].max = Date.parse(data.maxDate);
                plot.setupGrid();
                plot.draw();
            });
}

$('#accordion').accordion({
    collapsible: true,
    active: false,
    heightStyle: 'content'
});
