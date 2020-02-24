<template>
  <div id="container">
    <div id="image-section">
      <img id="intro-img" src="../assets/pwa/intro.png" alt />
    </div>
    <div id="text-section">
      <p class="odk-title" id="title">Object Detection Kit</p>
      <p class="body-1">Zorg voor schone straten door te scannen tijdens het rijden</p>
      <!-- <button id="add-button">Add to home screen</button> -->
      <b-button id="add-button">Add to home screen</b-button>
      <p class="body-1">
        Please
        <span id="add-to-home">‘add to homescreen’</span> to continue
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "browser-startpage",
  data() {
    return {};
  },
  methods: {
    checkAppMode() {
      let checkMedia = window.matchMedia("(display-mode: standalone)").matches;
      if (checkMedia) {
        console.log("This is running as standalone.");
        //If user downloaded pwa then he doesnt have to see this page
        this.$router.push({ path: "/pwa" });
      } else {
        console.log("This is running on the browser");
        // if (process.env.VUE_APP_APP_MODE) {
        //   console.log("development mode");
        //   this.$router.push({ path: "/pwa" });
        // }
      }
    },
    addToHs() {
      // const addBtn = document.getElementById("add-button");

      // addBtn.style.display = "none";
      this.deferredPrompt.prompt();
      // Wait for the user to respond to the prompt
      this.deferredPrompt.userChoice.then(choiceResult => {
        if (choiceResult.outcome === "accepted") {
          console.log("User accepted the A2HS prompt");
        } else {
          console.log("User dismissed the A2HS prompt");
        }
        this.deferredPrompt = null;
      });
    }
  },
  mounted() {
    // Init
    // IF USER DONT HAVE PWA DOWNLOADED ON MOBILE, TABLET OR PC/LAPTOP DEVICE THEY CANT ACCESS THE VIDEO STREAM
    this.checkAppMode();
    // this.addToHs();
    console.log("New app");
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
  height: 100%;
  justify-content: center;
  align-items: center;
  max-height: 896px;
  max-width: 414px;
  margin: 0 auto;
  position: relative;
  top: 3rem;
}

#container div {
  background: var(--second-white-color);
  width: 100%;
  height: 100%;
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

  #image-section {
    align-items: center;
  }

  #text-section {
    justify-content: center;
  }
}
</style>