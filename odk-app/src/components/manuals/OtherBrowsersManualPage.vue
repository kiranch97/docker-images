<template>
  <div id="container">
    <header>
      <img src="../../assets/manual/logo-2.png" />
    </header>
    <div v-for="manual in manuals" v-bind:key="manual.id" id="supported-browsers">
      <p class="body-2">{{manual.title}}</p>
      <p class="odk-title">{{manual.browserName}}</p>
      <p class="title-2 attention">{{manual.attention}}</p>
      <p class="body-1 recommendation">{{manual.recommendation}}</p>
      <p class="body-1 body">{{manual.body}}</p>
    </div>
    <OtherDevicesManuals :otherBrowser="otherBrowser"/>
    <!-- <div id="unsupported-browsers"></div>  -->
    <footer>&copy; 2020 ODK by Gemeente Amsterdam</footer>
  </div>
</template>

<script>

import OtherDevicesManuals from "./OtherDevicesManuals"

export default {
  name: "other-browsers-manual-page",
    components: {
    OtherDevicesManuals
  },
  data() {
    return {
      otherBrowser: true,
      manuals: [
        {
          title: "How to install PWA?",
          browserName: "Other browsers, Android",
          attention: "Attention:",
          recommendation: "We recommend you to use Chrome, Firefox or Edge.",
          body: "Unfortunately we cannot garantee the optimal functionality of this PWA in all browsers. Please use Chrome, Firefox or Edge for tested results.",
        }
      ]
    };
  },
  methods: {},
  mounted() {
  }
};
</script>

<style scoped>
header {
  width: 100%;
  background: var(--main-purple-color);
  height: 5rem !important;
  position: absolute;
  display: flex;
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

.attention{
    padding: 1rem 0;
    /* border: 2px solid black; */
}

.recommendation{
    /* border: 2px solid red; */
}

.body{
/* border: 2px solid blue; */
padding: 1rem 0;
/* padding-bottom: 2.5rem; */
}

.body-1 {
  /* padding-bottom: 1rem; */
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