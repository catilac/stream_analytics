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
    var redraw = false;
    return function(data) {
        console.log(data);
        var _data = JSON.parse(data);

        var width = 420,
            barHeight = 20;

        var x = d3.scale.linear()
            .domain([0, d3.max(_data, function(d){ return d[1]; })])
            .range([0, width]);

        var chart = d3.select('.chart')
            .attr("width", width)
            .attr("height", barHeight * _data.length);

        var bar = chart.selectAll("g")
            .data(_data)
          .enter().append("g")
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
    };
}

$(function() {
    rtht = new RealTimeHashTags();
    rtht.setOnReceive(processD3Factory());
    rtht.start();
});
