<template>
  <odk-container>
    <div
      class="image-section"
      aria-hidden="true"
    >
      <onboarding-animation style="transform: translateX(-15%)" />
    </div>

    <div class="text-section">
      <div class="text-section-header">
        <h1 class="odk-title">Voordat u begint</h1>
      </div>

      <div class="text-section-buttons">
        <b-button
          expanded
          outlined
          rounded
          type="is-primary"
          :class="{ 'check-item-complete' : landscapeOrientation}"
        >
          <div>
            <div style="width: 32px;">
              <svg
                v-if="landscapeOrientation"
                class="check-icon"
                width="24px"
                height="24px"
                viewBox="0 0 24 24"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink"
              >
                <g
                  class="Icons/Check"
                  stroke="none"
                  stroke-width="1"
                  fill="none"
                  fill-rule="evenodd"
                >
                  <path
                    class="Path-3"
                    d="M18.3050227,6.62611652 C18.7931781,6.13796116 19.5846343,6.13796116 20.0727897,6.62611652 C20.5284013,7.0817282 20.5587755,7.80154862 20.163912,8.29238813 L20.0727897,8.39388348 L11.2351441,17.2315291 C10.5919276,17.8747456 9.57257605,17.9125818 8.88510839,17.3450379 L8.76027032,17.2315291 L4.91611652,13.3873753 C4.42796116,12.8992199 4.42796116,12.1077637 4.91611652,11.6196083 C5.3717282,11.1639967 6.09154862,11.1336225 6.58238813,11.528486 L6.68388348,11.6196083 L9.997,14.933 L18.3050227,6.62611652 Z"
                    fill="#2F1C50"
                  />
                </g>
              </svg>
            </div>
            <span>Houd uw telefoon liggend</span>
          </div>
        </b-button>

        <b-button
          class="loc-check-button"
          expanded
          outlined
          rounded
          type="is-primary"
          :class="{ 'check-item-complete' : locationPermission}"
          @click="askLocPermission()"
        >
          <div>
            <div style="width: 32px;">
              <svg
                v-if="locationPermission"
                class="check-icon"
                width="24px"
                height="24px"
                viewBox="0 0 24 24"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink"
              >
                <g
                  class="Icons/Check"
                  stroke="none"
                  stroke-width="1"
                  fill="none"
                  fill-rule="evenodd"
                >
                  <path
                    class="Path-3"
                    d="M18.3050227,6.62611652 C18.7931781,6.13796116 19.5846343,6.13796116 20.0727897,6.62611652 C20.5284013,7.0817282 20.5587755,7.80154862 20.163912,8.29238813 L20.0727897,8.39388348 L11.2351441,17.2315291 C10.5919276,17.8747456 9.57257605,17.9125818 8.88510839,17.3450379 L8.76027032,17.2315291 L4.91611652,13.3873753 C4.42796116,12.8992199 4.42796116,12.1077637 4.91611652,11.6196083 C5.3717282,11.1639967 6.09154862,11.1336225 6.58238813,11.528486 L6.68388348,11.6196083 L9.997,14.933 L18.3050227,6.62611652 Z"
                    fill="#2F1C50"
                  />
                </g>
              </svg>
            </div>
            <span class="buttonspan">GPS-locatie inschakelen</span>
          </div>
        </b-button>

        <b-button
          expanded
          outlined
          rounded
          type="is-primary"
          :disabled="!locationPermission"
          :class="{ 'check-item-complete' : camPermission}"
          class="camera-button camera-check-button"
          @click="askCamPermission()"
        >
          <div>
            <div style="width: 32px;">
              <svg
                v-if="camPermission"
                class="check-icon"
                width="24px"
                height="24px"
                viewBox="0 0 24 24"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink"
              >
                <g
                  class="Icons/Check"
                  stroke="none"
                  stroke-width="1"
                  fill="none"
                  fill-rule="evenodd"
                >
                  <path
                    class="Path-3"
                    d="M18.3050227,6.62611652 C18.7931781,6.13796116 19.5846343,6.13796116 20.0727897,6.62611652 C20.5284013,7.0817282 20.5587755,7.80154862 20.163912,8.29238813 L20.0727897,8.39388348 L11.2351441,17.2315291 C10.5919276,17.8747456 9.57257605,17.9125818 8.88510839,17.3450379 L8.76027032,17.2315291 L4.91611652,13.3873753 C4.42796116,12.8992199 4.42796116,12.1077637 4.91611652,11.6196083 C5.3717282,11.1639967 6.09154862,11.1336225 6.58238813,11.528486 L6.68388348,11.6196083 L9.997,14.933 L18.3050227,6.62611652 Z"
                    fill="#2F1C50"
                  />
                </g>
              </svg>
            </div>
            <span class="buttonspan2">Camera inschakelen</span>
          </div>
        </b-button>
      </div>
      <p class="tip">Als u deze stappen niet volgt, zal u ODK niet kunnen gebruiken</p>
    </div>
  </odk-container>
</template>

<script>
import OnboardingAnimation from "./OnboardingAnimation.vue";

export default {
  name: "ChecklistPage",

  components: {
    "onboarding-animation": OnboardingAnimation,
  },

  data () {
    return {
      /// UI properties.
      landscapeOrientation: false,
      locationPermission: false,
      camPermission: false,
      blockProgress: false,

      // Geolocation coordinates.
      positionLa: null,
      positionLo: null,
      currentCameraOption: null,

      // Front camera resolution.
      rearCamResolution: {
        width: 1280,
        height: 720,
      },
    };
  },

  mounted () {
    // Check if locationPermission, camPermission en landscape orientation are active.
    this.checkAppMode();

    this.checkAppOrientation();
    window.addEventListener("resize", this._.debounce(this.checkAppOrientation, 250));

    // Use data of previous login, but generate a new streamId for the session.
    this.checkCredentials();

    // @todo If `this.checkAppOrientation = true` go to /client immedietly
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

    checkAppOrientation () {
      if (window.innerWidth > window.innerHeight) {
        console.log("orientation = landscape");
        this.landscapeOrientation = !this.landscapeOrientation;
      } else {
        console.log("orientation = portrait");
        this.landscapeOrientation = false;
      }

      this.checkAllPermission();
    },

    askLocPermission () {
      if (this.blockProgress) return;

      if ("geolocation" in navigator) {
        navigator.geolocation.watchPosition(
          this.updatePosition,
          this.locationAccessDenied,
        );

        this.locationPermission = !this.locationPermission;
      } else {
        console.log("Geolocation is not supported by this browser.");
      }

      this.checkAllPermission();
    },

    locationAccessDenied (error) {
      if (error.code == error.PERMISSION_DENIED) {
        this.locationPermission = false;
        console.log("Geolocation permission was denied.");
        this.goToNextView("/clear-storage");
      }
    },

    updatePosition: function (position) {
      this.positionLa = position.coords.latitude;
      this.positionLo = position.coords.longitude;
    },

    askCamPermission () {
      if (this.blockProgress) return;

      const curScope = this;

      this.currentConstraints = {
        video: {
          facingMode: this.currentCameraOption,
          width: this.rearCamResolution.width,
          height: this.rearCamResolution.height,
        },
        audio: false,
      };

      navigator.mediaDevices
        .getUserMedia(this.currentConstraints)
        .then(mediaStream => {
          // Stop the stream
          const tracks = mediaStream.getTracks();
          tracks[0].stop();
        })
        .then(() => {
          curScope.camPermission = !curScope.camPermission;
        })
        .then(() => {
          curScope.checkAllPermission();
        })
        .catch((err) => {
          console.log("==> Error occured in 'showStream':/ Permission denied");
          console.error(err);
          this.goToNextView("/clear-storage");
        })
      ;
    },

    checkAllPermission () {
      if (
        this.locationPermission &&
        this.camPermission &&
        this.landscapeOrientation
      ) {
        this.goToNextView("/client");
      }
    },

    goToNextView (route) {
      this.blockProgress = true;

      setTimeout(() => {
        this.blockProgress = false;
        this.$router.push(route);
      }, 1000);
    },
  },
};
</script>

<style lang="scss" scoped>
.image-section {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50%;
}

.text-section {
  display: flex;
  flex-direction: column;
  align-self: center;
  justify-content: space-between;
  padding: 2.5rem;
  height: 50%;

  &-header {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    width: 100%;
    text-align: left;

    .odk-title {
      margin-bottom: 1rem;
    }
  }

  &-buttons {
    .button {
      margin-bottom: .75rem;

      div:first-of-type {
        display: flex;
        align-items: center;
        width: 100%;
      }
    }
  }
}

.check-item-complete {
  background: rgba(105, 89, 133, 0.6) !important;
}

.check-icon {
  margin-right: 0.25rem;
}

.tip {
  margin-top: 0.5rem;
  text-align: left;
  font-size: 0.875rem;
}

@media (orientation: landscape) {
  .image-section {
    width: 45%;
    height: auto;
  }

  .text-section {
    width: 55%;
    height: 100%;
    max-height: 414px;
  }
}
</style>
