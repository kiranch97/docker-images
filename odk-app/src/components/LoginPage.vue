<template>
  <div id="container">
    <qrcode-stream :camera="camera" :track="track" @decode="sendWebSocketsMsg" @init="onInit">
      <div v-if="validationWaiting" class="validation-waiting">
        Scan a given QR-code
        <b-icon pack="fas" icon="qrcode" size="is-large"></b-icon>
      </div>
      <div v-if="validationPending" class="validation-pending">Validation in progress...</div>
      <div v-if="validationFailure" class="validation-failure">Try again</div>
      <div v-if="validationSuccess" class="validation-success">Success</div>
    </qrcode-stream>
  </div>
</template>

<script>
import { QrcodeStream } from "vue-qrcode-reader";

export default {
  name: "login-page",

  components: { QrcodeStream },

  data() {
    return {
      userType: null,
      apiWebsocketUrl: process.env.VUE_APP_API_WS_URL,
      camera: "front",

      // For QR
      track: false,
      isValid: "waiting"
    };
  },

  // ----

  computed: {
    validationWaiting() {
      return this.isValid === "waiting" && this.camera === "front";
    },

    // ----

    validationPending() {
      return this.isValid === "waiting" && this.camera === "off";
    },

    // ----

    validationSuccess() {
      return this.isValid === true;
    },

    // ----

    validationFailure() {
      return this.isValid === false;
    }
  },

  // ----

  methods: {
    checkNotIDUsertype() {
      if (
        typeof localStorage.appId == "undefined" ||
        localStorage.appId == null ||
        !localStorage.userType
      ) {
        this.$router.push("/recommendation");
      }
    },

    // ----

    setupWebSockets() {
      //Setup connection with Websocket server URL:PORT/ENDPOINT
      let websocketUrl = this.apiWebsocketUrl + "/stream-login";
      this.websocketConnection = new WebSocket(websocketUrl);
      //Websocket events
      this.websocketConnection.onmessage = this.receiveWebSocketsMsg;
    },

    // ----

    async sendWebSocketsMsg(content) {
      this.turnCameraOff();
      await this.timeout(1000);

      // Send QR-code result to API for verification
      let data = {
        message: content
      };

      this.websocketConnection.send(JSON.stringify(data));
    },

    // ----

    async receiveWebSocketsMsg(e) {
      //Websocket event when Message sent by the server
      let response = JSON.parse(e.data);

      if (response.success) {
        this.isValid = true;
        await this.timeout(1000);
        this.$router.push("/client");
      } else {
        this.isValid = false;
        await this.timeout(1000);
        this.turnCameraOn();
      }
    },

    // ----

    onInit(promise) {
      promise.catch(console.error).then(this.resetValidationState);
    },

    // ----

    resetValidationState() {
      this.isValid = "waiting";
    },

    // ----

    turnCameraOn() {
      this.camera = "front";
    },

    // ----

    turnCameraOff() {
      this.camera = "off";
    },

    // ----

    timeout(ms) {
      return new Promise(resolve => {
        window.setTimeout(resolve, ms);
      });
    }
  },

  // ----

  mounted() {
    this.checkNotIDUsertype();
    this.setupWebSockets();
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
  background: var(--second-white-color);
  display: flex;
  flex-direction: row;
  /* justify-content: center;
  align-items: center; */
  overflow: hidden !important;
}

.validation-success,
.validation-failure,
.validation-pending,
.validation-waiting {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.7);
  text-align: center;
  font-family: "Open Sans", sans-serif !important;
  font-weight: 600;
  font-size: 1.4rem;
  padding: 10px;
  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
  align-items: center;
}
.validation-waiting {
  background: none;
  color: var(--yellow-color);
}
.validation-pending {
  color: var(--dark-blue-color);
}
.validation-success {
  color: var(--success-color);
}
.validation-failure {
  color: var(--error-color);
}

.icon {
  padding-top: 3rem;
}
</style>