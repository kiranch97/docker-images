<template>
  <div id="app">
    <transition name="fade" mode="out-in">
      <router-view />
    </transition>
  </div>
</template>

<script>
export default {
  name: "App",

  beforeMount () {
    this.setViewportHeight();

    window.addEventListener("resize", this._.debounce(this.setViewportHeight, 250));
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
  display: flex;
  align-items: flex-start;
  background: var(--color-grey-light);
  width: 100%;
  height: 100%;
  text-align: center;
  line-height: 1.5;
  color: var(--color-blue-dark);
  font-size: 1rem;
  font-weight: 400;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
}

h1,
.odk-title {
  line-height: 2;
  color: var(--color-blue-dark);
  font-size: 1.5rem;
  font-weight: 700;
}

h2,
.title-2 {
  line-height: 2;
  color: var(--color-blue-dark);
  font-size: 1.125rem;
  font-weight: 700;
}

p,
.body-1 {
  margin-block-start: 1em;
  margin-block-end: 1em;
}

.body-2 {
  line-height: 1.875;
  color: var(--color-blue-dark);
  font-size: 0.875rem;
  font-weight: 600;
}

.caption-1 {
  color: var(--color-blue-dark);
  font-size: 0.85em;
  font-weight: 400;
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
