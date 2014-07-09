function isNumber(obj) {
    return !isNaN(parseFloat(obj));
}

if (typeof tablesorter !== 'undefined' && $.isFunction(tablesorter)) {
    $('.tablesorter').tablesorter();
}

if (typeof stickyTableHeaders !== 'undefined' && $.isFunction(stickyTableHeaders)) {
    $('table').stickyTableHeaders();
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

if ($('table#index')) {
    $('table#index').remove();

    $('body').append('<div id="tabs"><ul><li><a href="#graph-tab">Graph</a>'
           + '</li><li><a href="#table-tab">Table</a></li></ul>'
           + '<div id="graph-tab"></div><div id="table-tab"></div></div>');
    $('#graph-tab').append('<div id="flot-graph" style="width: 500px;'
           + ' height: 300px; float: left"></div>');
    $('#graph-tab').append('<div id="flot-graph-legend" style="float: left"></div>');
    $.getJSON($SCRIPT_ROOT + '/_allmetrics', {},
            function(data) {
                var select = $('<select></select>').attr('id', 'metrics-list');
                $.each(data.non_ts_metrics, function(i, el) {
                    select.append('<option value="' + el + '">' + el + '</option>');
                });
                var table_select = $('<select></select>').attr('id', 'table-metrics-list');
                $.each(data.metrics, function(i, el) {
                    table_select.append('<option value"' + el + '">' + el + '</option>');
                });
                $('#graph-tab').append(select);
                $('#table-tab').append(table_select);
            });
    $('#add-to-graph').click();
    $('#graph-tab').append('<button id="add-to-graph">Add metric to graph</button>');
    $('#table-tab').append('<button id="display-in-table">Display metric in table</button>');
}

if (typeof $.plot !== 'undefined' && $.isFunction($.plot)) {
    $('#add-to-graph').click(function() {
        var metric = $('select#metrics-list').val();
        $.getJSON($SCRIPT_ROOT + '/_' + metric + 'graphdata', {},
            function(data) {
                var pairs = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]];
                var labels = [];
                for (var i=0; i < data.res.length; i++) {
                    var x = Date.parse(data.res[i][0].replace('-', '-').substring(0, data.res[i][0].indexOf(' ')));
                    var ys = data.res[i].slice(1);
                    for (var j=0; j < ys.length; j++) {
                        if (isNumber(ys[j])) {
                            pairs[j].push([x, ys[j]]);
                            if (i==0) {
                                labels.push(data.cols.slice(1)[j]);
                            }
                        }
                    }
                }
                var d = [];
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
                    }
                };
                $.plot(('#flot-graph'), d, options);
            });
    });
}

$('#display-in-table').click(function() {
    var table_metric = $('select#table-metrics-list').val();
    $.getJSON($SCRIPT_ROOT + '/_' + table_metric + 'gettable', {},
        function(data) {
            $('#table').remove();
            var headers = data.headers;
            var rows = data.rows;
            table = '<table id="table"><tr>'
            for (var i=0; i < headers.length; i++) {
                var header = headers[i];
                table += '<th>' + header + '</th>';
            }
            table += '</tr>';
            for (var i=0; i < rows.length; i++) {
                row = rows[i];
                table += '<tr>';
                for (var j=0; j < row.length; j++) {
                    col = row[j];
                    table += '<td>' + col + '</td>';
                }
                table += '</tr>';
            }
            $('#table-tab').append(table);
        });
});

$('#tabs').tabs();
