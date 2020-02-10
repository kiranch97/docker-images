<template>
  <div id="setup-images">
    <!-- animation div, used by Lottie -->
    <div ref="container" id="animLottie" class="animation"></div>
    <!-- robot animation trigger, used by ScrollMagic -->
    <div id="trigger" class="scene"></div>
  </div>
</template>

<script>
import { animationData } from "../assets/animation/data";

export default {
  data() {
    return {
      robotAnim: null
    };
  },

  mounted() {
    const { container } = this.$refs;
    //animation data
    var setupAnimData = {
      container: container,
      renderer: "svg",
      loop: true,
      autoplay: true,
      animationData: animationData
    };

    console.log(setupAnimData);

    // this.robotAnim = bodymovin.loadAnimation(setupAnimData);


  }
};
</script>

<style scoped>
.animation {
  position: relative;
  top: 20%;
  width: 100%;
  height: auto;
}

#setup-images {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: auto;
}

@media only screen and (max-width: 1023px) {
  #setup-images {
    width: 90%;
  }
}
</style>
