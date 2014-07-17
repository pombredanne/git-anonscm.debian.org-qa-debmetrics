/*
 * Parts from jquery.flot.hiddengraphs.js
 */

(function($) {
    function init(plot) {
        function addMetricLabel(plot, options) {
            if (!options.metrics) {
                return;
            }

            var p = plot.getPlaceholder();
            for (var i=0; i < options.indices.length; i++) {
                var tr = '<tr><td class="legendColorBox2"></td>'
                       + '<td class="legendLabel2"><span class="graphlabel2">'
                       + options.metrics[i] + '</span>' + '</td></tr>';
                var legend = $('#flot-graph-legend');
                legend.find('tr').eq(options.indices[i]).before(tr);

                var graphlabel = legend.find('.legendLabel2').eq(i);
                var legendColorBox = legend.find('.legendColorBox2').eq(i);

                setHideAction(graphlabel);
                setHideAction(legendColorBox);
            }
        }

        function addDeleteButtons(plot, options) {
            var legend = $('#flot-graph-legend');
            legend.find('tr').each(function(i) {
                $(this).prepend('<td><button class="close"></button></td>');
            });
            addDeleteFunction();
        }
        
        function addDeleteFunction() {
            var legend = $('#flot-graph-legend');
            legend.find('button').each(function(i) {
                if ($(this).parent().siblings().eq(0).attr('class') === 'legendColorBox') {
                    $(this).unbind('click').click(function() {
                        updateIndices(i);
                        removeColumnGraph(index2col(i));
                        if (lastColumn(i)) {
                            removeColumnGraph('package_stats');
                        }
                    });
                } else {
                    $(this).unbind('click').click(function() {
                        metric = $(this).parent().parent().text();
                        init = metric2index(metric, 0);
                        var end = metric2index(metric, 1);
                        for (var j=init+1; j < end; j++) {
                            col = index2col(init+1);
                            updateIndices(init+1);
                            if ($.inArray(col, options.metrics) === -1) {
                                removeColumnGraph(col);
                            }
                        }
                        updateIndices(init+1);
                        removeColumnGraph(metric);
                        addDeleteFunction();
                    });
                }
            });
        }

        function lastColumn(i) {
            var ret = false;
            var indices2 = options.indices.slice(0);
            indices2.push(options.lastIndex);
            for (var j=0; j < indices2.length-1; j++) {
                if ((indices2[j+1]-indices2[j]) === 1) {
                    ret = true;
                }
            }
            return ret;
        }

        function index2col(i) {
            var legend = $('#flot-graph-legend');
            var col = legend.find('tr').eq(i).text();
            return col;
        }

        function metric2index(metric, increment) {
            metricIndex = options.metrics.indexOf(metric);
            var index = options.indices[metricIndex + increment];
            if (index != null) {
                return index;
            } else {
                return options.lastIndex;
            }
        }

        function setHideAction(elem) {
            elem.unbind('click').click(function() {
                for (var i=metric2index($(this).text(), 0); i < metric2index($(this).text(), 1); i++) {
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
            addDeleteButtons(plot, options);
        });
    }

    var options = {metrics: ['default'], indices: [0]};

    $.plot.plugins.push({
        init: init,
        options: options,
        name: 'superlegends',
        version: '0.0.1'
    });
})(jQuery);
