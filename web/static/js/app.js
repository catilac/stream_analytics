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

$(function() {
    rtht = new RealTimeHashTags();
    rtht.start();
});
