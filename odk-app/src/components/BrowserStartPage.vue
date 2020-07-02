<template>
  <div id="container">
    <div id="image-section">
      <img id="intro-img" src="../assets/pwa/intro.png" alt>
    </div>

    <div id="text-section">
      <p id="title" class="odk-title">Object Detection Kit</p>
      <p class="body-1">Zorg voor schone straten door te scannen tijdens het rijden</p>
      <b-button id="add-button">Add to home screen</b-button>

      <!-- SUPPORTED BROWSERS MANUAL -->
      <div v-if="activeVendor === 'chrome' || activeVendor === 'firefoxAndroid'">
        <p class="body-1">
          <span id="add-to-home">Add to homescreen</span> to continue
        </p>
        <router-link :to="{ name:'installation-manual', params: { activeVendor } }">
          <p class="link">How to install a PWA?</p>
        </router-link>
      </div>

      <!-- UNSUPPORTED BROWSERS MANUAL -->
      <div v-else-if="activeVendor === 'iOS'">
        <p class="body-1">Not supported by iOS</p>
        <router-link :to="{ name:'installation-manual', params: { activeVendor } }">
          <p class="link">Why?</p>
        </router-link>
      </div>

      <div v-else>
        <p class="body-1">Please use another browser</p>
        <router-link :to="{ name:'installation-manual', params: { activeVendor } }">
          <p class="link">Which one?</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { isChrome, isFirefox, isMSEdge, isAndroid, isiOS } from "../utils/detect";

export default {
  name: "BrowserStartPage",

  data () {
    return {
      activeVendor: null,
    };
  },

  mounted () {
    // IF USER DONT HAVE PWA DOWNLOADED ON MOBILE, TABLET OR PC/LAPTOP DEVICE THEY CANT ACCESS THE VIDEO STREAM
    this.checkAppMode();
    this.checkBrowserType();

    // PWA INSTALLATION POP-UP
    let deferredPrompt;
    const addBtn = document.getElementById("add-button");
    addBtn.style.display = "none";

    window.addEventListener("beforeinstallprompt", e => {
      e.preventDefault();
      deferredPrompt = e;
      addBtn.style.display = "block";

      addBtn.addEventListener("click", () => {
        // Hide our user interface that shows our A2HS button
        addBtn.style.display = "none";

        // Show the prompt
        deferredPrompt.prompt();

        // Wait for the user to respond to the prompt
        deferredPrompt.userChoice.then(choiceResult => {
          if (choiceResult.outcome === "accepted") {
            console.log("User accepted the A2HS prompt");
          } else {
            console.log("User dismissed the A2HS prompt");
          }

          deferredPrompt = null;
        });
      });
    });
  },

  methods: {
    checkAppMode () {
      const checkMedia = window.matchMedia("(display-mode: standalone)").matches;

      if (checkMedia) {
        console.log("This is running as standalone.");

        // If user installed the PWA he does not have to see this page.
        this.$router.push("/recommendation");
      } else {
        console.log("This is running on the browser");
      }
    },

    checkBrowserType () {
      if (isChrome() || isMSEdge()) {
        console.log("Browser: Chromium");
        this.activeVendor = "chrome";
      }

      else if (isFirefox() && isAndroid()) {
        console.log("Browser: Mozilla Firefox, Device: Android");
        this.activeVendor = "firefoxAndroid";
      }

      else if (isiOS()) {
        console.log("Browser: WebKit-based, Device: iOS");
        this.activeVendor = "iOS";
      }

      else {
        console.log("Device and browser: unsupported");
        this.activeVendor = "others";
      }
    },
  },
};
</script>

<style scoped>
.odk-title {
  margin-bottom: 0.75rem;
  line-height: 2.125rem;
  color: var(--dark-blue-color);
  font-size: 1.5rem;
  font-weight: 800;
}

.body-1 {
  padding-right: 46px;
  padding-left: 47px;
  line-height: 26px;
  color: var(--dark-blue-color);
  font-family: "Open Sans", sans-serif;
  font-size: 1rem;
  font-weight: 400;
}

#container {
  display: flex;
  position: relative;
  top: 3rem;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  background: var(--second-white-color);
  width: 100%;
  max-width: 414px;
  height: 100vh;
  max-height: 896px;
}

#text-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 20rem;
}

#text-section :nth-child(2) {
  margin-bottom: 1.75rem;
}

#add-to-home {
  font-weight: 700;
}

.link {
  color: var(--pink-color) !important;
  text-decoration: underline !important;
  padding-top: 1rem;
}

#image-section {
  display: flex;
  justify-content: center;
}

#intro-img {
  max-height: 426px;
  width: 80%;
  object-fit: contain;
  margin-top: 2.375rem;
  margin-bottom: 2.375rem;
}

#add-button {
  display: flex;
  align-items: center;
  margin-bottom: 1.75rem;
  border: 2px solid var(--second-purple-color) !important;
  color: var(--second-purple-color) !important;
  font-family: "Open Sans", sans-serif !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
}

@media (max-width: 1024px) and (orientation: portrait) {
  #container div {
    background: var(--second-white-color);
    width: 100%;
    height: 100%;
  }

  #container {
    top: 0;
  }

  #image-section {
    display: flex;
    justify-content: center;
  }
}

@media (max-width: 1024px) and (orientation: landscape) {
  #container {
    top: 0;
    flex-direction: row;
    max-width: none;
    max-height: none;
  }

  #container #image-section {
    align-items: center;
  }

  #text-section {
    justify-content: center;
    align-items: center;
  }
}
</style>
