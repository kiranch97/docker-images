<template>
  <div id="clock">
    <span class="time">{{ time }}</span>

    <!-- <div class="btn-container">
      <a @click="start()" id="start">Start</a>
      <a @click="stop()" id="stop">Stop</a>
      <a @click="reset()" id="reset">Reset</a>
    </div> -->
  </div>
</template>

<script>
export default {
  name: "Streamtime",

  data: function () {
    return {
      time: "00:00:00",
      timeBegan: null,
      timeStopped: null,
      stoppedDuration: 0,
      started: null,
      running: false,
    };
  },

  methods: {
    start () {
      if (this.running) return;

      if (this.timeBegan === null) {
        this.reset();
        this.timeBegan = new Date();
      }

      if (this.timeStopped !== null) {
        this.stoppedDuration += new Date() - this.timeStopped;
      }

      this.started = setInterval(this.clockRunning, 10);
      this.running = true;
    },

    stop () {
      this.running = false;
      this.timeStopped = new Date();
      clearInterval(this.started);
    },

    reset () {
      this.running = false;
      clearInterval(this.started);
      this.stoppedDuration = 0;
      this.timeBegan = null;
      this.timeStopped = null;
      this.time = "00:00:00";
    },

    clockRunning () {
      var currentTime = new Date(),
        timeElapsed = new Date(
          currentTime - this.timeBegan - this.stoppedDuration
        ),
        hour = timeElapsed.getUTCHours(),
        min = timeElapsed.getUTCMinutes(),
        sec = timeElapsed.getUTCSeconds()
        // ms = timeElapsed.getUTCMilliseconds();
      ;

      this.time =
        this.zeroPrefix(hour, 2) +
        ":" +
        this.zeroPrefix(min, 2) +
        ":" +
       this.zeroPrefix(sec, 2);
        // "." +
        // this.zeroPrefix(ms, 3);
    },

    zeroPrefix (num, digit) {
      var zero = "";
      for (var i = 0; i < digit; i++) {
        zero += "0";
      }
      return (zero + num).slice(-digit);
    },
  },
};
</script>

<style lang="scss" scoped>
.clock {
  outline: none;
}
</style>
