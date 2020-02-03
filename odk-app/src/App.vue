<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'app',
}
</script>

<style>
:root {
  --main-purple-color: #3a225d;
  --second-purple-color: #2f1c50;
  --red-color: #e1524a;
  --pink-color: #c83760;
  --yellow-color: #f6d365;
  --white-color: #ffffff;
  --second-white-color: #f9f8fa;
  --black-color: #000000;
  --dark-blue-color: #151522;
  --error-color: #c83737;
  --success-color: #37c88b;
  --grey-color: #e2dee9;
  --grey-blue-color: #9891a4;
}

html, body {
  background: var(--grey-color);
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden!important;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  width: 100%;
  height: 100%;
}

</style>
