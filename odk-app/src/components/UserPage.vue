<template>
  <div class="container">
    <div class="qr-section">
      <login-page />
    </div>

    <div class="text-section">
      <div class="header-section">
        <p class="caption-1">Laatste stap</p>
        <h1>Scan je QR-Code</h1>
        <p style="margin-top: .5em;">
          Als chauffeur van de Gemeente Amsterdam heb je een QR-Code ontvangen om je account mee te gebruiken. Houd deze voor de camera om verder te gaan.
        </p>
      </div>

      <div class="buttons-section">
        <p style="margin-bottom: .5em;">
          <span class="link" @click="saveId('demo')">Ik ben geen gemeente chauffeur</span>
        </p>
        <p
          class="caption-1"
        >
          Als je voor deze optie kiest zal de gescande data niet worden opgeslagen.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import LoginPage from "./LoginPage";

export default {
  name: "UserPage",

  components: {
    "login-page": LoginPage,
  },
  data () {
    return {
      buttonDisabled: true,
    };
  },
  mounted () {
    // Init
    //IF USER IN BROWSER AND development mode is off redirect them to BrowserStartPage
    this.checkAppMode();
    //IF USER HAS LOGGED IN BEFORE use that info but GENERATE NEW streamId for new session
    this.checkCredentials();
  },

  // ----

  methods: {
    checkAppMode () {
      const checkMedia = window.matchMedia("(display-mode: standalone)").matches;

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

    checkCredentials () {
      if (localStorage.streamId) {
        localStorage.streamId = this.generateId();
        this.$router.push({
          name: "streaming-client",
          params: { uniqueId: localStorage.streamId },
        });
      }
    },

    generateId () {
      const uniqueId = Math.random()
        .toString(32)
        .substring(3);
      return uniqueId;
    },

    // ----

    saveId (user) {
      if (user == "worker") {
        localStorage.userType = "waste_department";
      } else {
        const uniqueId = this.generateId();
        localStorage.userType = "demo";
        this.$router.push({
          name: "streaming-client",
          params: { uniqueId: uniqueId },
        });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  position: relative;
  margin: 0 auto;
  background: var(--color-white-bis);
  width: 100vw;
  max-width: 896px;
  height: 100vh;
  max-height: 414px;
}

.qr-section {
  z-index: 0;
  width: 50%;
  height: 100%;
}

.text-section {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  z-index: 1;
  padding: 2.5rem 4rem 2.5rem 3rem;
  width: 50%;
  height: 100%;
}

.header-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  width: 100%;
  text-align: left;
}

.caption-1 {
  margin: 0;
}

.buttons-section {
  display: flex;
  flex-direction: column;
  width: 100%;
  text-align: left;
}
</style>
