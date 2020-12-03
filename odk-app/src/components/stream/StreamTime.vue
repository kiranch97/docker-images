<template>
  <div id="stream-timer">
    <div id="status-box" :class="{ 'is-streaming': isStreaming }">
      <div v-if="isStreaming && !webSocketDisconnected" class="blink-icon" />
      <DefaultLoader
        id="loader"
        :loading="webSocketDisconnected"
        :size="25"
        color="white"
      />
      <div
        ref="streamtimer"
        class="streamtimer"
      >
        <span class="time">{{ time }}</span>

        <!-- <div class="btn-container">
          <a @click="start()" id="start">Start</a>
          <a @click="pause()" id="pause">Pause</a>
          <a @click="reset()" id="reset">Reset</a>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import { DefaultLoader } from "vue-spinners-css";
import { eventBus } from "@/main";

export default {
  name: "Streamtime",

  components: {
    DefaultLoader,
  },

  props: {
    webSocketDisconnected: {
      type: Boolean,
      default: false,
    },
    isStreaming: {
      type: Boolean,
      default: true,
    },
  },

  data () {
    return {
      time: "00:00:00",
      timeBegan: null,
      timeStopped: null,
      pausedDuration: 0,
      started: null,
      running: false,
    };
  },

  mounted () {
    // EventBus for receiving control usage
    eventBus.$on("startStreamTimer", () => {
      this.start();
    });
    eventBus.$on("pauseStreamTimer", () => {
      this.pause();
    });
    eventBus.$on("resetStreamTimer", () => {
      this.reset();
    });
  },

  methods: {
    start () {
      if (this.running) return;

      if (this.timeBegan === null) {
        this.reset();
        this.timeBegan = new Date();
      }

      if (this.timeStopped !== null) {
        this.pausedDuration += new Date() - this.timeStopped;
      }

      this.started = setInterval(this.clockRunning, 10);
      this.running = true;
    },

    pause () {
      this.running = false;
      this.timeStopped = new Date();
      clearInterval(this.started);
    },

    reset () {
      this.running = false;
      clearInterval(this.started);
      this.pausedDuration = 0;
      this.timeBegan = null;
      this.timeStopped = null;
      this.time = "00:00:00";
    },

    clockRunning () {
      var currentTime = new Date(),
        timeElapsed = new Date(
          currentTime - this.timeBegan - this.pausedDuration
        ),
        hour = timeElapsed.getUTCHours(),
        min = timeElapsed.getUTCMinutes(),
        sec = timeElapsed.getUTCSeconds()
      ;

      this.time =
        this.zeroPrefix(hour, 2) +
        ":" +
        this.zeroPrefix(min, 2) +
        ":" +
       this.zeroPrefix(sec, 2);
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
#stream-timer {
  flex: 0 1 auto;
  width: 100%;
  display: flex;
  justify-content: center;

  #status-box {
    position: relative;
    width: 10rem;
    height: 2rem;
    background: rgba(76, 71, 85, 0.8);
    top: 1rem;
    border-radius: 30px;
    display: flex;
    justify-content: center;
    align-items: center;

    &.is-streaming {
      background-color: var(--color-error);
    }

    .blink-icon {
      position: absolute;
      width: 0.6rem;
      height: 0.6rem;
      background: var(--color-white);
      left: 1.3rem;
      border-radius: 50%;
      box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
      animation: blink 1.5s infinite both;
      z-index: 10;
    }

    #loader {
      position: absolute;
      width: 18px;
      height: 18px;
      left: 0.7rem;
    }

    .streamtimer {
      color: var(--color-white);
      font-size: 1rem;
      font-weight: 600;
      text-shadow: 0 2px 3px rgba(0, 0, 0, 0.6);
      outline: none;
    }
  }
}

@-webkit-keyframes blink {
  0%,
  50%,
  100% {
    opacity: 1;
  }

  25%,
  75% {
    opacity: 0;
  }
}

@keyframes blink {
  0%,
  50%,
  100% {
    opacity: 1;
  }

  25%,
  75% {
    opacity: 0;
  }
}
</style>
