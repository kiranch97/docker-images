<template>
  <div id="container">
    <div id="qr-section">
      <login-page></login-page>
    </div>
    <div id="text-section">
      <div id="header-section">
        <p class="caption-1">Laatste stap</p>
        <p class="odk-title" id="title">Scan je QR-Code</p>
        <p
          class="body-1"
        >Als chauffeur van de Gemeente Amsterdam heb je een QR-Code ontvangen om je account mee te gebruiken. Houd deze voor de camera om verder te gaan.</p>
      </div>
      <div id="buttons-section">
        <p class="link" @click="saveId('demo')">Ik ben geen gemeente chauffeur</p>
        <p
          class="caption-1"
        >Als je voor deze optie kiest zal de gescande data niet worden opgeslagen.</p>
      </div>
    </div>
  </div>
</template>

<script>
import LoginPage from "./LoginPage";

export default {
  name: "user-page",
  data() {
    return {
      buttonDisabled: true
    };
  },

  // ----

  components: {
    "login-page": LoginPage
  },

  // ----

  methods: {
    checkAppMode() {
      let checkMedia = window.matchMedia("(display-mode: standalone)").matches;
      if (checkMedia) {
        console.log("This is running as standalone.");
      } else {
        console.log("This is running on the browser");
        // process.env.VUE_APP_APP_MODE
        //   ? console.log("development mode")
        //   : this.$router.push({ path: "/" });
      }
    },

    // ----

    checkCredentials() {
      if (localStorage.streamId) {
        localStorage.streamId = this.generateId();
        this.$router.push({
          name: "streaming-client",
          params: { uniqueId: localStorage.streamId }
        });
      }
    },

    // ----

    generateId() {
      let uniqueId = Math.random()
        .toString(32)
        .substring(3);
      return uniqueId;
    },

    // ----

    saveId(user) {
      if (user == "worker") {
        localStorage.userType = "waste_department";
      } else {
        let uniqueId = this.generateId();
        localStorage.userType = "demo";
        this.$router.push({
          name: "streaming-client",
          params: { uniqueId: uniqueId }
        });
      }
    }
  },
  mounted() {
    // Init
    //IF USER IN BROWSER AND development mode is off redirect them to BrowserStartPage
    this.checkAppMode();
    //IF USER HAS LOGGED IN BEFORE use that info but GENERATE NEW streamId for new session
    this.checkCredentials();
  }
};
</script>

<style scoped>
#container {
  position: relative;
  width: 100vw;
  height: 100vh;
  max-width: 896px;
  max-height: 414px;
  margin: 0 auto;
  /* padding: 0 2rem 0 0; */
  background: var(--second-white-color);
  display: flex;
}

#qr-section {
  width: 50%;
  height: 100%;
  z-index: 0;
}

#text-section {
  width: 50%;
  height: 100%;
  padding: 2.5rem 4rem 2.5rem 3rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  z-index: 1;
}

#header-section {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  text-align: left;
  width: 100%;
  margin-top: 2rem;
}

#buttons-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  text-align: left;
}

.link {
  color: var(--pink-color) !important;
  text-decoration: underline !important;
  margin-bottom: 0.25rem;
}

.link:hover {
  cursor: pointer;
}

@media screen and (max-width: 756px) {
  .odk-title {
    font-size: 1.25rem !important;
  }

  .body-1 {
    font-size: 0.9rem !important;

    line-height: 1.25rem !important;
  }

  #yellow-button,
  #transparent-button {
    font-size: 0.9rem;
  }
}

@media screen and (max-width: 660px) {
}
</style>
