$(function() {
    $('input#date').bind('change', function() {
        $.getJSON($SCRIPT_ROOT + '/_sources', {
            d: $('input#date').val()
        }, function(data) {
            $('#graph').attr('src', data.graph);
            $('#title').text(data.name);
            $('input#date').datepicker('option', 'maxDate', data.maxDate);
            $('input#date').datepicker('option', 'minDate', data.minDate);
        });
        return false;
    });
});

$('input#date').datepicker({
    dateFormat: "yy-mm-dd",
});
