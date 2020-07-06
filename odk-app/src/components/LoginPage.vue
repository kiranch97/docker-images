<template>
  <div id="qr-container">
    <qrcode-stream
      :camera="camera"
      :track="track"
      @decode="sendQR"
      @init="onInit"
    >
      <div v-if="validationWaiting" class="validation-waiting">
        <div id="yellow-square" />
      </div>
      <div v-else-if="validationPending" class="validation-pending">Wordt gevalideerd...</div>
      <div v-else-if="validationFailure" class="validation-failure">Probeer opniew</div>
      <div v-else class="validation-success">Gevalideerd</div>
    </qrcode-stream>
  </div>
</template>

<script>
import { QrcodeStream } from "vue-qrcode-reader";

export default {
  name: "LoginPage",

  components: { QrcodeStream },

  data () {
    return {
      userType: null,
      apiHttpUrl: process.env.VUE_APP_API_HTTP_URL,
      camera: "front",

      // For QR
      track: false,
      isValid: "waiting",
    };
  },

  // ----

  computed: {
    validationWaiting () {
      return this.isValid === "waiting" && this.camera === "front";
    },

    // ----

    validationPending () {
      return this.isValid === "waiting" && this.camera === "off";
    },

    // ----

    validationSuccess () {
      return this.isValid === true;
    },

    // ----

    validationFailure () {
      return this.isValid === false;
    },
  },

  // ----

  methods: {
    generateId () {
      const uniqueId = Math.random()
        .toString(32)
        .substring(3);
      return uniqueId;
    },

    // ----

    async sendQR (content) {
      this.turnCameraOff();
      await this.timeout(1000);

      fetch(this.apiHttpUrl + "/authorized_login?credential_string=" + content, {
        method: "GET",
      })
        .then(response => {
          return response.json();
        })
        .then(results => {
          if (results.success) {
            this.isValid = true;
            localStorage.vehicleType = results.vehicle_type;
            localStorage.driverPhoneNumber = results.driver_phone_number;

            const uniqueId = this.generateId();
            localStorage.userType = "worker";

            this.timeout(1000);

            this.$router.push({
              name: "streaming-client",
              params: { uniqueId: uniqueId },
            });
          } else {
            this.isValid = false;
            this.timeout(1000);
            this.turnCameraOn();
          }
        });
    },

    // ----

    onInit (promise) {
      promise.catch(console.error).then(this.resetValidationState);
    },

    // ----

    resetValidationState () {
      this.isValid = "waiting";
    },

    // ----

    turnCameraOn () {
      this.camera = "front";
    },

    // ----

    turnCameraOff () {
      this.camera = "off";
    },

    // ----

    timeout (ms) {
      return new Promise(resolve => {
        window.setTimeout(resolve, ms);
      });
    },
  },
};
</script>

<style scoped>
#qr-container {
  width: 100%;
  height: 100%;
}

.validation-success,
.validation-failure,
.validation-pending,
.validation-waiting {
  position: absolute;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.7);
  text-align: center;
  font-family: "Open Sans", sans-serif !important;
  font-weight: 600;
  font-size: 1.4rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.validation-waiting {
  background: none;
  border: 50px solid rgba(0, 0, 0, 0.5);
}

#yellow-square {
  width: 100%;
  height: 100%;
  border: 3px solid var(--yellow-color);
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
