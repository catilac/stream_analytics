var RealTimeHashTags = function(n) {
    if (n) {
        this.n = n;
    }
    this.n = 15;

    /* start()
     * receive updates from server
     */
    this.start = function() {
        this._getUpdates();
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
        this._getUpdates();
        return;
    };

    this.setOnReceive = function(func) {
        if (func && typeof(func) === "function") {
            this._onReceive = func;
        }
    };
};

$(function() {
    rtht = new RealTimeHashTags();
    rtht.setOnReceive(function(data) {
        console.log(data);
    });
    rtht.start();
});
