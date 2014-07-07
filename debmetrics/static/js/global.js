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

$(function() {
    $('input#date').bind('change', function() {
        $.getJSON($SCRIPT_ROOT + '/_' + metric, {
            d: $('input#date').val()
        }, function(data) {
            $('#graph').attr('src', data.graph);
            $('.title').each(function() {$(this).text(data.name)});
        });
        return false;
    });
});

$.getJSON($SCRIPT_ROOT + '/_' + metric + 'minmax', {},
        function(data) {
            $('input#date').datepicker('option', 'maxDate', data.maxDate);
            $('input#date').datepicker('option', 'minDate', data.minDate);
        });

if (typeof datepicker !== 'undefined' && $.isFunction(datepicker)) {
    $('input#date').datepicker({
        dateFormat: "yy-mm-dd",
    });
}

$('table#index').remove();

$('body').append('<div id="flot-graph" style="width: 500px; height: 300px; float: left"></div>');
$('body').append('<select id="metrics-list"><option value="vcs">vcs</option></select>');
$('body').append('<button id="add-to-graph">Add metric to graph</button>')

if (typeof $.plot !== 'undefined' && $.isFunction($.plot)) {
    $('#add-to-graph').click(function() {
        var metric = $('select#metrics-list').val();
        $.getJSON($SCRIPT_ROOT + '/_' + metric + 'graphdata', {},
            function(data) {
                var pairs = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]];
                for (var i=0; i < data.res.length; i++) {
                    var x = Date.parse(data.res[i][0].replace('-', '-').substring(0, data.res[i][0].indexOf(' ')));
                    var ys = data.res[i].slice(1);
                    for (var j=0; j < ys.length; j++) {
                        pairs[j].push([x, ys[j]]);
                    }
                }
                var d = [];
                for (var i=0; i < pairs.length; i++) {
                    d.push({label: data.cols.slice(1)[i], data: pairs[i]});
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
