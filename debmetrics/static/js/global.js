function isNumber(obj) {
    return !isNaN(parseFloat(obj));
}

if (typeof tabs !== 'undefined' && $.isFunction(tabs)) {
    $('#tabs').tabs();
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

    $('body').append('<div id="flot-graph" style="width: 500px; height: 300px; float: left"></div>');
    $.getJSON($SCRIPT_ROOT + '/_allmetrics', {},
            function(data) {
                var select = $('<select></select>').attr('id', 'metrics-list');
                $.each(data.metrics, function(i, el) {
                    select.append('<option value="' + el + '">' + el + '</option>');
                });
                $('body').append(select);
            });
    $('body').append('<button id="add-to-graph">Add metric to graph</button>');
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
                    }
                };
                $.plot($('#flot-graph'), d, options);
            });
    });
}

$('button#add-to-graph').click();
