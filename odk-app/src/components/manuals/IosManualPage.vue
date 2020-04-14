<template>
  <div id="container">
    <header>
      <router-link to="/">
        <img id="logo" src="../../assets/manual/logo-2.png" />
      </router-link>
    </header>
    <div v-for="manual in manuals" v-bind:key="manual.id" id="supported-browsers">
      <p class="body-2">{{manual.title}}</p>
      <p class="odk-title">{{manual.browserName}}</p>
      <p class="body-1 attention">{{manual.attention}}</p>
      <p class="body-1 recommendation">{{manual.recommendation}}</p>
      <p class="body-1 body">{{manual.body}}</p>
    </div>
    <OtherDevicesManuals :iosActive="iosActive" />
    <!-- <div id="unsupported-browsers"></div>  -->
    <footer>&copy; 2020 ODK by Gemeente Amsterdam</footer>
  </div>
</template>

<script>
import OtherDevicesManuals from "./OtherDevicesManuals";

export default {
  name: "Ios-manual-page",
  components: {
    OtherDevicesManuals
  },
  data() {
    return {
      iosActive: true,
      manuals: [
        {
          title: "How to install PWA?",
          browserName: "IOS",
          attention: "Attention:",
          recommendation:
            "At this moment you cannot use this app on IOS devices.",
          body:
            "Unfortunately video stream in a PWA is still not supported by any browser, in IOS. We recommend you to use Chrome, Firefox or Edge in an Android phone."
        }
      ]
    };
  },
  methods: {},
  mounted() {}
};
</script>

<style scoped>
header {
  width: 100%;
  background: var(--main-purple-color);
  height: 5rem !important;
  position: absolute;
  display: flex;
  align-items: center;
}

header img {
  object-fit: contain;
  padding-left: 1.5rem;
}

footer {
  width: 100%;
  height: 4rem;
  background: var(--main-purple-color);
  color: white;
  display: flex;
  position: absolute;
  bottom: 0;
  justify-content: center;
  align-items: center;
}

#wrapper {
  margin: 0 auto;
}

#container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  max-width: 414px;
  margin: 0 auto;
  position: relative;
  background: var(--second-white-color);
  text-align: left;
  overflow-y: auto;
}

#supported-browsers {
  padding: 0 1.5rem;
  margin-top: 7rem;
}

.attention {
  font-weight: 700 !important;
}

.body {
  padding: 1rem 0;
}

.body-2 {
  margin-bottom: 0.375rem;
}

.odk-title {
  margin-bottom: 2.125rem;
}

#icon {
  object-fit: contain;
  height: 2rem;
  position: relative;
  top: 0.5rem;
}

.image {
  object-fit: contain;
  width: 100%;
  border-radius: 12px;
}

@media (max-width: 1024px) and (orientation: portrait) {
  /* #container div {
    background: var(--second-white-color);
    width: 100%;
    height: 100%;
  } */

  #container {
    top: 0;
  }
}

@media (max-width: 1024px) and (orientation: landscape) {
  #container {
    flex-direction: row;
    top: 0;
    max-width: none;
    max-height: none;
  }
}
</style>