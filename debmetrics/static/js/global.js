$('#tabs').tabs();

$('.tablesorter').tablesorter();

$('table').stickyTableHeaders();

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

$('input#date').datepicker({
    dateFormat: "yy-mm-dd",
});
