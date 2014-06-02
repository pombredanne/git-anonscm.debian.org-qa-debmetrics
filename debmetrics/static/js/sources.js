$(function() {
    $('input#date').bind('change', function() {
        $.getJSON($SCRIPT_ROOT + '/_sources', {
            d: $('input#date').val()
        }, function(data) {
            $('#graph').attr('src', data.graph);
            $('.title').each(function() {$(this).text(data.name)});
        });
        return false;
    });
});

$.getJSON($SCRIPT_ROOT + '/_sourcesminmax', {},
        function(data) {
            $('input#date').datepicker('option', 'maxDate', data.maxDate);
            $('input#date').datepicker('option', 'minDate', data.minDate);
        });

$('#tabs').tabs();

$('input#date').datepicker({
    dateFormat: "yy-mm-dd",
});
