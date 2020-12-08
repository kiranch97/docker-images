<template>
  <div id="stream-speed">
    <p>Speed: {{ speedReadout }} km/h</p>

    <!-- Minimum driving speed changer -->
    <div class="stream-speed-div">
      <span>Min: </span>
      <div 
        class="stream-speed-div-control"
        @click="changeSpeed('min', 'down')" 
      >
        <img src="@/assets/ui/minus.svg">
      </div>
      <span>{{ minDrivingSpeed }}</span>
      <div 
        class="stream-speed-div-control"
        @click="changeSpeed('min', 'up')" 
      >
        <img src="@/assets/ui/plus.svg">
      </div>
      <div class="reset" @click="resetSpeed('min')" />
    </div>

    <!-- Maximum driving speed changer -->
    <div class="stream-speed-div">
      <span>Max: </span>
      <div 
        class="stream-speed-div-control"
        @click="changeSpeed('max', 'down')" 
      >
        <img src="@/assets/ui/minus.svg">
      </div>
      <span>{{ maxDrivingSpeed }}</span>
      <div 
        class="stream-speed-div-control"
        @click="changeSpeed('max', 'up')" 
      >
        <img src="@/assets/ui/plus.svg">
      </div>
      <div class="reset" @click="resetSpeed('max')" />
    </div>
  </div>
</template>

<script>
import { eventBus } from "@/main";

export default {
  name: "StreamControls",

  data () {
    return {
      minDrivingSpeed: process.env.VUE_APP_MINIMUM_DRIVING_SPEED,
      maxDrivingSpeed: process.env.VUE_APP_MAXIMUM_DRIVING_SPEED,
      speedReadout: 0.0000,
    };
  },

  mounted () {
    this.setSpeed();

    eventBus.$on("speedUpdated", (val) => {
      this.speedReadout = val;
    });
  },

  methods: {
    setSpeed () {
      if (localStorage.minSpeed && localStorage.maxSpeed) {
        this.minDrivingSpeed = parseInt(localStorage.minSpeed);
        this.maxDrivingSpeed = parseInt(localStorage.maxSpeed);
        return;
      }

      if (localStorage.minSpeed) {
        this.minDrivingSpeed = parseInt(localStorage.minSpeed);
        return;
      }

      if (localStorage.maxSpeed) {
        this.maxDrivingSpeed = parseInt(localStorage.maxSpeed);
        return;
      }

      this.minDrivingSpeed = parseInt(this.minDrivingSpeed);
      this.maxDrivingSpeed = parseInt(this.maxDrivingSpeed);
    },

    // ----

    changeSpeed (minOrMax, upOrDown) {
      // min up
      if (minOrMax === "min" && upOrDown === "up") {
        // prevent above max
        if (this.minDrivingSpeed == (this.maxDrivingSpeed - 1)) {
          return;
        }
        this.minDrivingSpeed += 1;
        eventBus.$emit("minSpeedChanged", this.minDrivingSpeed);
        return;
      }

      // min down
      if (minOrMax === "min" && upOrDown === "down") {
        // prevent negative number
        if (this.minDrivingSpeed == 0) {
          return;
        }
        this.minDrivingSpeed -= 1;
        eventBus.$emit("minSpeedChanged", this.minDrivingSpeed);
        return;
      }

      // max up
      if (upOrDown === "up") {
        this.maxDrivingSpeed += 1;
        eventBus.$emit("maxSpeedChanged", this.maxDrivingSpeed);
        return;
      }

      // max down
      // prevent below min
      if (this.maxDrivingSpeed == (this.minDrivingSpeed + 1)) {
        return;
      }
      this.maxDrivingSpeed -= 1;
      eventBus.$emit("maxSpeedChanged", this.maxDrivingSpeed);
    },

    // ----

    resetSpeed (minOrMax) {
      // min reset
      if (minOrMax === "min") {
        this.minDrivingSpeed = parseInt(process.env.VUE_APP_MINIMUM_DRIVING_SPEED);
        eventBus.$emit("minSpeedChanged", this.minDrivingSpeed);
        return;
      }

      // max reset
      this.maxDrivingSpeed = parseInt(process.env.VUE_APP_MAXIMUM_DRIVING_SPEED);
      eventBus.$emit("maxSpeedChanged", this.maxDrivingSpeed);
    },
  },
};
</script>

<style lang="scss" scoped>
#stream-speed {
  position: absolute;
  bottom: 0;
  padding: 0 1rem;
  background: var(--color-white);
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  font-size: 0.75rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  .stream-speed-div {
    height: 2rem;
    background: var(--color-grey-90);
    display: flex;
    justify-content: center;
    align-items: center;

    &:first-of-type {
      margin: 0.75rem 0 0.25rem 0;
    }

    &:last-of-type {
      margin: 0.25rem 0 0.75rem 0;
    }

    span:first-of-type {
      width: 3rem;
    }

    &-control {
      width: 2rem;
      height: 2rem;
      background: var(--color-warning);
      display: flex;
      justify-content: center;
      align-items: center;

      img {
        height: 60%;
      }
    }

    span:last-of-type {
      width: 4rem;
    }

    .reset {
      width: 1rem;
      height: 1rem;
      margin: 0 1rem;
      background: var(--color-error);
      border: 1px solid rgba(255, 255, 255, 0.5);
      border-radius: 50%;
    }
  }
}
</style>