$(function() {
    $('input#date').bind('input', function() {
        $.getJSON($SCRIPT_ROOT + '/_sources', {
            d: $('input#date').val()
        }, function(data) {
            $('#graph').attr('src', data.graph);
            $('#title').text(data.name);
        });
        return false;
    });
});
