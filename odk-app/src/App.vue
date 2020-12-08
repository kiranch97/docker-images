<template>
  <div id="app">
    <transition name="fade" mode="out-in">
      <router-view />
    </transition>
  </div>
</template>

<script>
import { pwaDiscardDetection } from "./utils/pwaFeatures";

export default {
  name: "App",

  beforeMount () {
    this.setViewportHeight();

    window.addEventListener("resize", this._.debounce(this.setViewportHeight, 250));

    pwaDiscardDetection();
  },

  methods: {
    setViewportHeight () {
      const vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty("--vh", `${vh}px`);
    },
  },
};
</script>

<style lang="scss">
@import "./styles/utilities";
@import "./styles/elements";

#app {
  -webkit-tap-highlight-color: transparent;
  display: flex;
  align-items: flex-start;
  background: var(--color-grey-light);
  width: 100%;
  height: 100%;
  text-align: center;
  line-height: 1.5;
  color: var(--color-dark);
  font-family: $family-sans-serif;
  font-size: $size-6;
  font-weight: 400;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
}

h1,
.odk-title {
  line-height: 1.5;
  color: var(--color-dark);
  font-size: $size-5;
  font-weight: $weight-bold;
}

h2,
.title-2 {
  line-height: 2;
  color: var(--color-dark);
  font-size: 1.125rem;
  font-weight: $weight-bold;
}

p {
  margin-top: 0.75rem;
}

.body-1 {
  color: var(--color-grey-40);
  font-size: $size-6;
  font-weight: $weight-normal;
}

.body-2 {
  line-height: 1.875;
  color: var(--color-dark);
  font-size: 0.875rem;
  font-weight: $weight-semibold;
}

.caption-1 {
  color: var(--color-dark);
  font-size: 0.75em;
  font-weight: $weight-normal;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 50ms ease-out;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
