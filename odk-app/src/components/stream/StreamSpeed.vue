<template>
  <div id="stream-speed">
    <p>Speed: {{ speedReadout }} km/h</p>
    <div id="stream-speed-numberinput">
      <div 
        id="stream-speed-numberinput-speed-up"
        @click="changeSpeed('min', 'down')" 
      >
        <img src="@/assets/ui/minus.svg">
      </div>
      <span>{{ minDrivingSpeed }}</span>
      <div 
        id="stream-speed-numberinput-speed-down"
        @click="changeSpeed('min', 'up')" 
      >
        <img src="@/assets/ui/plus.svg">
      </div>
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
      speedReadout: `0,0000`,
    };
  },

  mounted () {
    this.minDrivingSpeed = parseInt(this.minDrivingSpeed);
    this.maxDrivingSpeed = parseInt(this.maxDrivingSpeed);

    eventBus.$on("speedUpdated", (val) => {
      this.speedReadout = val;
    });
  },

  methods: {
    changeSpeed (minOrMax, upOrDown) {
      // min up
      if (minOrMax === "min" && upOrDown === "up") {
        this.minDrivingSpeed += 1;
        eventBus.$emit("minSpeedChanged", this.minDrivingSpeed);
        return;
      }

      // min down
      if (minOrMax === "min" && upOrDown === "down") {
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
      if (upOrDown === "down") {
        this.maxDrivingSpeed -= 1;
        eventBus.$emit("maxSpeedChanged", this.maxDrivingSpeed);
        return;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
#stream-speed {
  position: absolute;
  bottom: 0;
  padding: 0 1rem;
  background: #fff;
  font-size: 0.75rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  &-numberinput {
    width: 10rem;
    height: 2rem;
    margin: 0.75rem 0;
    background: var(--color-grey-90);
    display: flex;
    justify-content: space-between;
    align-items: center;

    &-speed-up, &-speed-down {
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
  }
}
</style>