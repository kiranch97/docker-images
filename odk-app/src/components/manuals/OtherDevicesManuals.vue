<template>
  <div id="other-manuals">
    <p class="title-2">Other devices or browsers</p>
    <ul>
      <router-link id="firefox" v-if="chromeActive || edgeActive || iosActive || otherBrowser" to="/firefox-manual">
        <li class="link">Firefox, Android</li>
      </router-link>
      <router-link id="chrome" v-if="firefoxActive || edgeActive || iosActive || otherBrowser" to="/chrome-manual">
        <li class="link">Chrome, Android</li>
      </router-link>
      <router-link id="edge" v-if="firefoxActive || chromeActive || iosActive || otherBrowser" to="/edge-manual">
        <li class="link">Edge, Android</li>
      </router-link>
      <router-link id="ios" v-if="chromeActive || firefoxActive || edgeActive || otherBrowser" to="/ios-manual">
        <li class="link">IOS</li>
      </router-link>
      <router-link id="other-browsers" v-if="chromeActive || firefoxActive || edgeActive || iosActive" to="/other-browsers-manual">
        <li class="link">Other browsers, Android</li>
      </router-link>
    </ul>
  </div>
</template>

<script>
export default {
    props: ["chromeActive", "firefoxActive", "edgeActive", "iosActive", "otherBrowser"],
};
</script>

<style scoped>
#other-manuals {
  height: 15rem;
  width: 100%;
  background: var(--grey-color);
  /* border: 2px solid black; */
  display: flex;
  flex-direction: column;
  padding: 0 1.5rem;
  padding-top: 2rem;
}

p .title-2 {
  text-align: left;
}

ul {
  /* border: 2px solid blue; */
  margin-bottom: 2rem;
}

.link {
  color: var(--pink-color) !important;
  text-decoration: underline !important;
  padding: 0.3rem 0;
}
</style>