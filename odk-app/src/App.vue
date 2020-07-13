<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style lang="scss">
@import "./styles/elements";

html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

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
</style>
