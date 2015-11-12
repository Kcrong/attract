function randomGenerator(low, high) {
    if (arguments.length < 2) {
        high = low;
        low = 0;
    }
    this.low = low;
    this.high = high;
    this.reset();
}

randomGenerator.prototype = {
    reset: function() {
        this.remaining = [];
        for (var i = this.low; i <= this.high; i++) {
            this.remaining.push(i);
        }
    },
    get: function() {
        if (!this.remaining.length) {
            this.reset();
        }
        var index = Math.floor(Math.random() * this.remaining.length);
        var val = this.remaining[index];
        this.remaining.splice(index, 1);
        return val;        
    }
}

var random = new randomGenerator(1, 20);
function getRandom(){ return new randomGenerator(1, 20);}
