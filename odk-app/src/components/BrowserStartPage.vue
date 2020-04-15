<template>
  <div id="container">
    <div id="image-section">
      <img id="intro-img" src="../assets/pwa/intro.png" alt />
    </div>
    <div id="text-section">
      <p class="odk-title" id="title">Object Detection Kit</p>
      <p class="body-1">Zorg voor schone straten door te scannen tijdens het rijden</p>
      <b-button id="add-button">Add to home screen</b-button>
      <!-- SUPPORTED BROWSERS MANUAL -->
      <div v-if="chromeActive">
        <p class="body-1">
          <span id="add-to-home">Add to homescreen</span> to continue
        </p>
        <router-link :to="{ name:'chrome-manual-page', params: {chromeActive: chromeActive } }">
          <p class="link">How to install a PWA?</p>
        </router-link>
      </div>
      <div v-if="firefoxActive">
        <p class="body-1">
          <span id="add-to-home">Add to homescreen</span> to continue
        </p>
        <router-link :to="{ name:'firefox-manual-page', params: {firefoxActive: firefoxActive } }">
          <p class="link">How to install a PWA?</p>
        </router-link>
      </div>
      <!-- UNSUPPORTED BROWSERS MANUAL -->
      <div v-if="iosActive">
        <p class="body-1">Not supported by IOS</p>
        <router-link to="ios-manual">
          <p class="link">Why?</p>
        </router-link>
      </div>
      <div v-if="otherBrowser">
        <p class="body-1">Please use another browser</p>
        <router-link :to="{name:'manual-page', params: {otherBrowser: otherBrowser}}">
          <p class="link">Which one?</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "browser-start-page",
  data() {
    return {
      chromeActive: false,
      iosActive: false,
      firefoxActive: false,
      otherBrowser: false
    };
  },
  methods: {
    checkAppMode() {
      let checkMedia = window.matchMedia("(display-mode: standalone)").matches;
      if (checkMedia) {
        console.log("This is running as standalone.");
        //If user downloaded pwa then he doesnt have to see this page
        this.$router.push("/recommendation");
      } else {
        console.log("This is running on the browser");
        // if (process.env.VUE_APP_APP_MODE) {
        //   console.log("development mode");
        //   this.$router.push("/recommendation");
        // }
      }
    },
    checkBrowserType() {
      // CHROME
      if (navigator.userAgent.indexOf("Chrome") != -1) {
        console.log("Google Chrome");
        this.chromeActive = true;
      }
      // FIREFOX
      else if (navigator.userAgent.indexOf("Firefox") != -1) {
        console.log("Mozilla Firefox");
        this.firefoxActive = true;
      }
      // EDGE
      else if (navigator.userAgent.indexOf("Edge") != -1) {
        console.log("Microsoft Edge");
        this.chromeActive = true;
      }
      // SAFARI
      else if (navigator.userAgent.indexOf("Safari") != -1) {
        console.log("Safari");
        this.iosActive = true;
      }
      // OTHERS
      else {
        console.log("Others");
        this.otherBrowser = true;
      }
    }
  },
  mounted() {
    // Init
    // IF USER DONT HAVE PWA DOWNLOADED ON MOBILE, TABLET OR PC/LAPTOP DEVICE THEY CANT ACCESS THE VIDEO STREAM
    this.checkAppMode();
    this.checkBrowserType();


    //PWA INSTALLATION POP-UP
    let deferredPrompt;
    const addBtn = document.getElementById("add-button");
    addBtn.style.display = "none";

    window.addEventListener("beforeinstallprompt", e => {
      e.preventDefault();
      deferredPrompt = e;
      addBtn.style.display = "block";

      addBtn.addEventListener("click", () => {
        // hide our user interface that shows our A2HS button
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
  }
};
</script>

<style scoped>
.odk-title {
  font-size: 1.5rem;
  font-weight: 800;
  line-height: 2.125rem;
  color: var(--dark-blue-color);
  margin-bottom: 0.75rem;
}

.body-1 {
  font-family: "Open Sans", sans-serif;
  font-size: 1rem;
  font-weight: 400;
  line-height: 26px;
  color: var(--dark-blue-color);
  /* width: 15rem; */
  padding-left: 47px;
  padding-right: 46px;
}

#container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  justify-content: center;
  align-items: center;
  max-height: 896px;
  max-width: 414px;
  margin: 0 auto;
  position: relative;
  top: 3rem;
  background: var(--second-white-color);
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
  /* width: 18rem; */
  /* height: 2.625rem; */
  color: var(--second-purple-color) !important;
  border: 2px solid var(--second-purple-color) !important;
  font-family: "Open Sans", sans-serif !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  display: flex;
  align-items: center;
  margin-bottom: 1.75rem;
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
    flex-direction: row;
    top: 0;
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