var RealTimeHashTags = function(n) {
    if (n) {
        this.n = n;
    }
    this.n = 15;

    /* start()
     * receive updates from server
     */
    this.start = function() {
        /* Start worker for getting updates */
        if (this._intervalId) {
            clearInterval(this._intervalId);
        }

        self._intervalId = setInterval(
            (function(self) {
                return function() {
                    self._getUpdates();
                };
            })(this),
            1000
        );
    };

    this._topUrl = function() {
        return "top/"+(this.n || 10);
    };

    this._getUpdates = function() {
        var topUrl = this._topUrl();
        $.ajax({
            url: topUrl,
        }).done(this._onReceive);
    };

    this._onReceive = function(data) {
        console.log("Received: ", data);
    };

    this.setOnReceive = function(func) {
        if (func && typeof(func) === "function") {
            this._onReceive = func;
        }
    };
};

function processD3Factory() {
    var width = 420,
        barHeight = 20;
    var chart = d3.select('.chart');

    var draw = function(data) {
        var _data = JSON.parse(data);
        var x = d3.scale.linear()
            .domain([0, d3.max(_data, function(d){ return d[1]; })])
            .range([0, width]);

        chart.attr("width", width)
            .attr("height", barHeight * _data.length);

        // HACK - just removing all data and then entering all of
        // in again.
        // TODO - deal with data diffs properly, and animate removals
        // and a shifting barchart
        chart.selectAll("g").data([]).exit().remove();
        var bar = chart.selectAll("g")
            .data(_data, function(d) { return d[0]+d[1]; });

        bar.enter().append("g")
            .attr("transform", function(d,i) {
                return "translate(0," + i * barHeight +")";
            });

        bar.append("rect")
            .attr("width", function(d) { return x(d[1]); })
            .attr("height", barHeight - 1);

        bar.append("text")
            .attr("x", function(d) { return x(d[1]) - 3; })
            .attr("y", barHeight / 2)
            .attr("dy", ".35em")
            .text(function(d) { return d[0] + "(" + d[1] + ")" });
    }


    return function(data) {
        draw(data);
    };
}

$(function() {
    rtht = new RealTimeHashTags();
    rtht.setOnReceive(processD3Factory());
    rtht.start();
});
