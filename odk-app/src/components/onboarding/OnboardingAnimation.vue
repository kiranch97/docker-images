<template>
  <div id="setup-images">
    <!-- Animation container, used by Lottie -->
    <div id="animLottie" ref="container" class="animation" />

    <!-- Robot animation trigger, used by ScrollMagic -->
    <div id="trigger" class="scene" />
  </div>
</template>

<script>
import { animationData } from "@/assets/animation/data";

export default {
  data () {
    return {
      robotAnim: null,
    };
  },

  mounted () {
    const { container } = this.$refs;

    // ScrollMagic options
    var setupAnimData = {
      container: container,
      renderer: "svg",
      loop: true,
      autoplay: true,
      animationData: animationData,
    };

    // eslint-disable-next-line no-undef
    this.robotAnim = bodymovin.loadAnimation(setupAnimData);
  },
};
</script>

<style scoped>
.animation {
  height: 100%;
}

#setup-images {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: -15%;
  height: 95vh;
}
</style>
