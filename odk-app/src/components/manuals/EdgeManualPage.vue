<template>
  <div id="container">
    <header>
      <img src="../../assets/manual/logo-2.png" />
    </header>
    <div v-for="manual in manuals" v-bind:key="manual.id" id="supported-browsers">
      <p class="body-2">{{manual.title}}</p>
      <p class="odk-title">{{manual.browserName}}</p>
      <div id="steps" v-for="step in manuals[0].steps" v-bind:key="step.id">
        <p class="title-2">{{step.step}}</p>
        <p class="body-1">
          {{step.instruction}}
          <img
            id="icon"
            v-if="step.icon"
            :src="require(`../../assets/manual/${step.icon}.png`)"
          />
        </p>
        <img class="image" :src="require(`../../assets/manual/${step.stepImage}.png`)" />
      </div>
    </div>
    <OtherDevicesManuals :edgeActive="edgeActive"/>
    <!-- <div id="unsupported-browsers"></div>  -->
    <footer>&copy; 2020 ODK by Gemeente Amsterdam</footer>
  </div>
</template>

<script>
import OtherDevicesManuals from "./OtherDevicesManuals";

export default {
  name: "manual-page",
  components: {
    OtherDevicesManuals
  },
  data() {
    return {
      edgeActive: true,
      manuals: [
        {
          title: "How to install PWA?",
          browserName: "Edge, Android",
          steps: [
            {
              step: "Step 1",
              instruction: "Tap",
              icon: "add2hs",
              stepImage: "firefox-1"
            },
            {
              step: "Step 2",
              instruction: "Confirm by tapping Add to Home screen.",
              stepImage: "firefox-2"
            },
            {
              step: "Step 3",
              instruction:
                "Choose by tapping Add automatically or by dragging the image to your home screen.",
              stepImage: "firefox-3"
            },
            {
              step: "Step 4",
              instruction:
                "Open app from home screen, as any other native app.",
              stepImage: "firefox-4"
            }
          ]
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
  /* margin-bottom: 5rem; */
  position: absolute;
  display: flex;
  /* border: 2px solid blue; */
}

header img {
  object-fit: contain;
  padding-left: 1.5rem;
}

footer {
  width: 100%;
  background: var(--main-purple-color);
  /* height: 5rem !important;  */
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  /* position: absolute; */
  /* bottom: 0; */
}

#wrapper {
  margin: 0 auto;
}

#container {
  display: flex;
  flex-direction: column;
  /* align-items: center; */
  width: 100%;
  height: 100%;
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

#steps {
  padding: 2rem 0;
  width: 100%;
}

.body-1 {
  padding-bottom: 1rem;
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