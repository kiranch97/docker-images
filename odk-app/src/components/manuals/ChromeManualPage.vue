<template>
  <div id="container">
    <header>
      <router-link to="/">
      <img id="logo" src="../../assets/manual/logo.svg" />
      </router-link>
    </header>
    <div v-for="manual in manuals" v-bind:key="manual.id" id="supported-browsers">
      <div id="step-item">
        <p class="body-2">{{manual.title}}</p>
        <p class="odk-title">{{manual.browserName}}</p>
        <div id="steps" v-for="step in manuals[0].steps" v-bind:key="step.id">
          <p class="title-2">{{step.step}}</p>
          <p class="body-1">{{step.instruction}}</p>
          <img class="image" :src="require(`../../assets/manual/${step.stepImage}.png`)" />
        </div>
      </div>
    </div>
    <OtherDevicesManuals :chromeActive="chromeActive"/>
    <!-- <div id="unsupported-browsers"></div>  -->
    <footer>&copy; 2020 ODK by Gemeente Amsterdam</footer>
  </div>
</template>

<script>

import OtherDevicesManuals from "./OtherDevicesManuals"

export default {
  name: "manual-page",
  components: {
    OtherDevicesManuals
  },
  data() {
    return {
      chromeActive: true,
      manuals: [
        {
          title: "How to install PWA?",
          browserName: "Chrome, Android",
          steps: [
            {
              step: "Step 1",
              instruction: "Open browser's settings",
              stepImage: "chrome-1"
            },
            {
              step: "Step 2",
              instruction: "Scroll down and tap Add to Home screen.",
              stepImage: "chrome-2"
            },
            {
              step: "Step 3",
              instruction: "Confirm by tapping Add.",
              stepImage: "chrome-3"
            },
            {
              step: "Step 4",
              instruction:
                "Open app from home screen, as any other native app.",
              stepImage: "chrome-4"
            }
          ]
        }
      ]
    };
  },
  methods: {},
  mounted() {
    console.log("Chrome is " + this.chromeActive);
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
  align-items: center;
}

header img {
  object-fit: contain;
  padding-left: 1.5rem;
}

footer {
  width: 100%;
  height: 4rem !important;
  background: var(--main-purple-color);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
}

#wrapper {
  margin: 0 auto;
}

#logo {
  height: 24px;
}

#container {
  display: flex;
  flex-direction: column;
  /* align-items: center; */
  width: 100%;
  height: auto;
  max-width: 414px;
  margin: 0 auto;
  position: relative;
  background: var(--second-white-color);
  text-align: left;
  overflow-y: auto;
}

#supported-browsers {
  padding: 0 1.5rem;
  margin-top: 7.375rem;
}

#steps {
  padding-bottom: 2.625rem;
  width: 100%;
}

.body-1 {
  padding-bottom: 1rem;
}

.body-2{
  margin-bottom: 0.375rem;
}

.odk-title{
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
    /* flex-direction: row; */
    top: 0;
    max-width: none;
    max-height: none;
  }

  /* #steps {
  padding: 2rem 0;
  width: 100%;
  display: flex;
  
} */


}
</style>