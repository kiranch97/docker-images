<template>
  <div class="container">
    <div class="image-section" aria-hidden="true">
      <img class="intro-img" src="../assets/pwa/intro.png" alt="Object Detection Kit abstract figure">
    </div>

    <div class="text-section">
      <h1>Object Detection Kit</h1>
      <p>Zorg voor schone straten door te scannen tijdens het rijden</p>

      <b-button
        v-if="pwaCapable"
        ref="addButton"
        type="is-primary"
        rounded
        outlined
        @click.native="clickAddAppButton"
      >
        Add to home screen
      </b-button>

      <!-- SUPPORTED BROWSERS MANUAL -->
      <div v-if="activeVendor === 'chrome' || activeVendor === 'edgeAndroid' || activeVendor === 'firefoxAndroid'">
        <p>
          <strong>Add to homescreen</strong> to continue
        </p>

        <p>
          <router-link :to="{ name:'installation-manual', params: { activeVendor } }">
            How to install a PWA?
          </router-link>
        </p>
      </div>

      <!-- UNSUPPORTED BROWSERS MANUAL -->
      <div v-else-if="activeVendor === 'iOS'">
        <p>Not supported by iOS</p>

        <p>
          <router-link :to="{ name:'installation-manual', params: { activeVendor } }">
            Why?
          </router-link>
        </p>
      </div>

      <div v-else-if="activeVendor === 'othersAndroid'">
        <p>Please use another browser</p>

        <p>
          <router-link :to="{ name:'installation-manual', params: { activeVendor } }">
            Which one?
          </router-link>
        </p>
      </div>

      <div v-else>
        <p>This app is intended for Android phones</p>

        <p>
          <router-link :to="{ name:'installation-manual', params: { activeVendor } }">
            Why?
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { startupCheck } from "../mixins/startupCheck";
import { isChrome, isFirefox, isMSEdge, isAndroid, isiOS } from "../utils/detect";

export default {
  name: "BrowserStartPage",

  mixins: [ startupCheck ],

  data () {
    return {
      activeVendor: null,
      pwaCapable: false,
      deferredPrompt: null,
    };
  },

  mounted () {
    // Without the PWA installed the user cannot access the video stream.
    this.checkAppMode();
    this.checkBrowserType();

    // PWA installation prompt event.
    window.addEventListener("beforeinstallprompt", e => {
      e.preventDefault();
      this.deferredPrompt = e;
      this.pwaCapable = true;
    });
  },

  methods: {
    clickAddAppButton () {
      // Show the deferred prompt.
      this.deferredPrompt.prompt();

      // Wait for the user to respond to the prompt.
      this.deferredPrompt.userChoice.then(choiceResult => {
        if (choiceResult.outcome === "accepted") {
          console.log("User accepted the A2HS prompt");
        } else {
          console.log("User dismissed the A2HS prompt");
        }

        this.deferredPrompt = null;
      });
    },

    checkBrowserType () {
      if (isAndroid() && isChrome()) {
        console.log("Browser: Chromium, Device: Android");
        this.activeVendor = "chrome";
      } else if (isAndroid() && isMSEdge()) {
        console.log("Browser: Microsoft Edge, Device: Android");
        this.activeVendor = "edgeAndroid";
      } else if (isAndroid() && isFirefox()) {
        console.log("Browser: Mozilla Firefox, Device: Android");
        this.activeVendor = "firefoxAndroid";
      } else if (isAndroid()) {
        console.log("Device and browser: unsupported");
        this.activeVendor = "othersAndroid";
      } else if (isiOS()) {
        console.log("Browser: WebKit-based, Device: iOS");
        this.activeVendor = "iOS";
      } else {
        console.log("Browser: n/a, Device: Not Android or iOS");
        this.activeVendor = "desktop";
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  position: relative;
  top: 3rem;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  margin: 0 auto;
  background: var(--color-grey-light);
  width: 100%;
  height: 90vh;
  max-height: 896px;
}

.image-section {
  display: flex;
  justify-content: center;
  height: 50%;
}

.intro-img {
  max-height: 426px;
  width: 80%;
  object-fit: contain;
  transform: translate(-20%, -5%);
}

.text-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 8%;
  height: 50%;
  min-height: 20rem;
}

.button {
  margin: 1.5rem auto;
}

@media (max-width: 1024px) and (orientation: portrait) {
  .container {
    top: 0;
  }

  .image-section {
    display: flex;
    justify-content: center;
  }
}

@media (max-width: 1024px) and (orientation: landscape) {
  .container {
    top: 0;
    flex-direction: row;
  }

  .container .image-section {
    align-items: center;
  }

  .text-section {
    justify-content: center;
    align-items: center;
  }
}
</style>
