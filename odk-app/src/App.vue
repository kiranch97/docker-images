<template>
  <div id="app">
    <!-- <onboarding></onboarding> -->
    <router-view></router-view>
  </div>
</template>

<script>

import Onboarding from './components/Onboarding';

export default {
  name: 'app',
  components: {
    "onboarding": Onboarding
  },

}
</script>

<style>

html, body {
  background: silver;
  margin: 0;
  padding: 0;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

</style>
