function isNumber(obj) {
    return !isNaN(parseFloat(obj));
}

$.tablesorter.addParser({
    id: 'customDate',
    is: function(s) {
        return /\d{1,4}}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}.\d{1,6}/.test(s);
    },
    format: function(s) {
        s = s.replace(/\-/g," ");
        s = s.replace(/:/g," ");
        s = s.replace(/\./g," ");
        s = s.split(" ");
        return $.tablesorter.formatFloat(new Date(s[0], s[1]-1, s[2], s[3], s[4], s[5]).getTime() + parseInt(s[6]));
    },
    type: 'numeric'
});

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

if ($('table#index').length > 0) {
    $('table#index').remove();

    $('#content').append('<div id="graph-table-container"></div>');
    /*$('<div id="tabs" class="cf"><ul><li><a href="#graph-tab">Graph</a>'
           + '</li><li><a href="#table-tab">Table</a></li></ul>'
           + '<div id="graph-tab"></div><div id="table-tab"></div></div>').insertBefore('footer');*/
    $('#graph-table-container').append('<div id="flot-graph" style="width: 500px;'
           + ' height: 300px; float: left"></div>');
    $('#graph-table-container').append('<div id="flot-graph-legend" style="float: left"></div>');
    $.getJSON($SCRIPT_ROOT + '/_allmetrics', {},
            function(data) {
                var select = $('<select></select>').attr('id', 'metrics-list');
                $.each(data.metrics, function(i, el) {
                    select.append('<option value"' + el + '">' + el + '</option>');
                });
                select.insertBefore('#add-metric');
            });
    $('#graph-table-container').append('<button id="add-metric">Add metric</button>');
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
    $('#xaxis-start').datepicker();
    $('#xaxis-end').datepicker();
}

var metrics = [];
var indices = [];
var index = 0;
var lastIndex;

$('#add-metric').click(function() {
    var metric = $('select#metrics-list').val();
    if ($.inArray(metric, metrics) === -1) {
        metrics.push(metric);
        indices.push(index);
        addToGraph();
    }
    displayInTable();
});

$('#remove-metrics').click(removeAllMetrics);

$('#resize-graph').click(resizeGraph);

$('#update-xaxis-range').click(updateXaxisRange);

var d = [];
var plot;

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
            });
    }
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
    plot.setData(d);
    plot.setupGrid();
    plot.draw();
    $('#table').remove();
    $('#csvLink').remove();
}

function displayInTable() {
    var table_metric = $('select#metrics-list').val();
    $.getJSON($SCRIPT_ROOT + '/_' + table_metric + 'gettable', {},
        function(data) {
            $('#table').remove();
            $('#csvLink').remove();
            var headers = data.headers;
            var rows = data.rows;
            table = '<div id="table-container" style="clear: both;"><table id="table" class="tablesorter"><thead><tr>'
            for (var i=0; i < headers.length; i++) {
                var header = headers[i];
                table += '<th><div class="drag-handle">&#9776;</div>' + header + '</th>';
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
            $('.tablesorter').tablesorter({
                dateFormat: 'yyyymmdd'
            });
            $('#table').stickyTableHeaders();
            $('#table').dragtable({dragHandle: '.drag-handle'});
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

$('#accordion').accordion({
    collapsible: true,
    active: false
});
