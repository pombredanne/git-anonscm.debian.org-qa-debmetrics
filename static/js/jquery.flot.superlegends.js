/*
 * Parts from jquery.flot.hiddengraphs.js
 */

(function($) {
    function init(plot) {
        function addMetricLabel(plot, options) {
            if (!options.metric) {
                return;
            }

            var p = plot.getPlaceholder();
            var tr = '<tr><td class="legendColorBox2"></td>'
                   + '<td class="legendLabel2"><span class="graphlabel2">'
                   + options.metric + '</span>' + '</td></tr>';
            var legend = $('#flot-graph-legend');
            legend.find('tbody').first().prepend(tr);

            var graphlabel = legend.find('.legendLabel2').first();
            var legendColorBox = legend.find('.legendColorBox2').first();

            setHideAction(graphlabel);
            setHideAction(legendColorBox);
        }

        function setHideAction(elem) {
            elem.unbind('click').click(function() {
                for (var i=0; i < $(this).parent().siblings().length; i++) {
                    labelClicked($(this).parent().siblings().eq(i).text());
                }
            });
        }

        function labelClicked(label) {
            plotLabelClicked(label);
            plot.setData(plot.getData());
            plot.setupGrid();
            plot.draw();
        }

        function findPlotSeries(label) {
            var plotdata = plot.getData();
            for (var i = 0; i < plotdata.length; i++) {
                if (plotdata[i].label == label) {
                    return plotdata[i];
                }
            }
            return null;
        }

        function plotLabelClicked(label, mouseOut) {
            var series = findPlotSeries(label);
            if (!series) {
                return;
            }

            var switchedOff = false;
            if (typeof series.points.oldShow === "undefined") {
                series.points.oldShow = false;
            }
            if (typeof series.lines.oldShow === "undefined") {
                series.lines.oldShow = false;
            }
            if (series.points.show && !series.points.oldShow) {
                series.points.show = false;
                series.points.oldShow = true;
                switchedOff = true;
            }
            if (series.lines.show && !series.lines.oldShow) {
                series.lines.show = false;
                series.lines.oldShow = true;
                switchedOff = true;
            }
            if (switchedOff) {
                series.oldColor = series.color;
                series.color = "#fff";
            } else {
                var switchedOn = false;
                if (!series.points.show && series.points.oldShow) {
                    series.points.show = true;
                    series.points.oldShow = false;
                    switchedOn = true;
                }
                if (!series.lines.show && series.lines.oldShow) {
                    series.lines.show = true;
                    series.lines.oldShow = false;
                    switchedOn = true;
                }
                if (switchedOn) {
                    series.color = series.oldColor;
                }
            }
        }


        plot.hooks.draw.push(function(plot, ctx) {
            options = plot.getOptions();
            addMetricLabel(plot, options);
        });
    }

    var options = {metric: 'default'};

    $.plot.plugins.push({
        init: init,
        options: options,
        name: 'superlegends',
        version: '0.0.1'
    });
})(jQuery);
