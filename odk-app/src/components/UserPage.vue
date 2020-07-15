<template>
  <odk-container>
    <div class="qr-section">
      <login-page />
    </div>

    <div class="text-section">
      <div class="text-section-header">
        <p class="caption-1">Laatste stap</p>
        <h1>Scan je QR-Code</h1>
        <p style="margin-top: .5em;">
          Als chauffeur van de Gemeente Amsterdam heb je een QR-Code ontvangen om je account mee te gebruiken. Houd deze voor de camera om verder te gaan.
        </p>
      </div>

      <div class="text-section-buttons">
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
  </odk-container>
</template>

<script>
export default {
  name: "UserPage",

  components: {
    LoginPage: () => import("./LoginPage"),
  },

  data () {
    return {
      buttonDisabled: true,
    };
  },

  mounted () {
    // If user in browser and development mode is off redirect them to BrowserStartPage.
    this.checkAppMode();

    // If user has logged in before use that info but generate new streamid for a new session.
    this.checkCredentials();
  },

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
.qr-section {
  z-index: 0;
  height: 50%;
}

.text-section {
  display: flex;
  flex-direction: column;
  align-self: center;
  justify-content: space-between;
  z-index: 1;
  padding: 2rem;
  height: 50%;

  &-header {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    width: 100%;
    text-align: left;

    &-buttons {
      display: flex;
      flex-direction: column;
      width: 100%;
      text-align: left;
    }

    .caption-1 {
      margin: 0;
    }
  }
}

@media (orientation: landscape) {
  .qr-section {
    align-self: center;
    width: 45%;
    height: 100%;
    max-height: 414px;
  }

  .text-section {
    padding: 1rem 1.5rem;
    width: 55%;
    height: 100%;
    max-height: 414px;

    .caption-1:first-of-type {
      display: none;
    }
  }
}

@media (orientation: landscape) and (min-width: 680px) {
  .qr-section {
    width: 50%;
  }

  .text-section {
    padding: 2.5rem 4rem 2.5rem 3rem;
    width: 50%;

    .caption-1:first-of-type {
      display: initial;
    }
  }
}
</style>
