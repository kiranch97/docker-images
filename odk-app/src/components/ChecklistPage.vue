<template>
  <div id="container">
    <div id="image-section">
      <onboarding-animation></onboarding-animation>
    </div>
    <div id="text-section">
      <div id="header-section">
        <p class="odk-title" id="title">Before start streaming</p>
      </div>
      <div id="buttons-section">
        <b-button
          :class="{ 'check-item-complete' : landscapeOrientation}"
          rounded
          id="gitlab-button"
          size="is-medium"
        >
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
            <g id="Icons/Check" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
              <path
                d="M18.3050227,6.62611652 C18.7931781,6.13796116 19.5846343,6.13796116 20.0727897,6.62611652 C20.5284013,7.0817282 20.5587755,7.80154862 20.163912,8.29238813 L20.0727897,8.39388348 L11.2351441,17.2315291 C10.5919276,17.8747456 9.57257605,17.9125818 8.88510839,17.3450379 L8.76027032,17.2315291 L4.91611652,13.3873753 C4.42796116,12.8992199 4.42796116,12.1077637 4.91611652,11.6196083 C5.3717282,11.1639967 6.09154862,11.1336225 6.58238813,11.528486 L6.68388348,11.6196083 L9.997,14.933 L18.3050227,6.62611652 Z"
                id="Path-3"
                fill="#2F1C50"
              />
            </g>
          </svg>
          Keep the screen landscape
        </b-button>

        <b-button
          rounded
          id="gitlab-button"
          size="is-medium"
          :class="{ 'check-item-complete' : locationPermission}"
          @click="askLocPermission()"
        >
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
            <g id="Icons/Check" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
              <path
                d="M18.3050227,6.62611652 C18.7931781,6.13796116 19.5846343,6.13796116 20.0727897,6.62611652 C20.5284013,7.0817282 20.5587755,7.80154862 20.163912,8.29238813 L20.0727897,8.39388348 L11.2351441,17.2315291 C10.5919276,17.8747456 9.57257605,17.9125818 8.88510839,17.3450379 L8.76027032,17.2315291 L4.91611652,13.3873753 C4.42796116,12.8992199 4.42796116,12.1077637 4.91611652,11.6196083 C5.3717282,11.1639967 6.09154862,11.1336225 6.58238813,11.528486 L6.68388348,11.6196083 L9.997,14.933 L18.3050227,6.62611652 Z"
                id="Path-3"
                fill="#2F1C50"
              />
            </g>
          </svg>
          Enable GPS location
        </b-button>

        <b-button
          :class="{ 'check-item-complete' : camPermission}"
          @click="askCamPermission()"
          rounded
          id="gitlab-button"
          size="is-medium"
        >
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
            <g id="Icons/Check" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
              <path
                d="M18.3050227,6.62611652 C18.7931781,6.13796116 19.5846343,6.13796116 20.0727897,6.62611652 C20.5284013,7.0817282 20.5587755,7.80154862 20.163912,8.29238813 L20.0727897,8.39388348 L11.2351441,17.2315291 C10.5919276,17.8747456 9.57257605,17.9125818 8.88510839,17.3450379 L8.76027032,17.2315291 L4.91611652,13.3873753 C4.42796116,12.8992199 4.42796116,12.1077637 4.91611652,11.6196083 C5.3717282,11.1639967 6.09154862,11.1336225 6.58238813,11.528486 L6.68388348,11.6196083 L9.997,14.933 L18.3050227,6.62611652 Z"
                id="Path-3"
                fill="#2F1C50"
              />
            </g>
          </svg>Enable Camera
        </b-button>
      </div>
      <p
        class="body-1"
        id="title"
      >In case you deny access, this app won't work until you delete cache storage</p>
    </div>
  </div>
</template>

<script>
import OnboardingAnimation from "./OnboardingAnimation.vue";
export default {
  name: "checklist-page",
  data() {
    return {
      landscapeOrientation: false,
      locationPermission: false,
      camPermission: false,
      positionLa: null,
      positionLo: null,
      currentCameraOption: null,
      rearCamResolution: {
        width: 1280,
        height: 720
      }
    };
  },
  components: {
    "onboarding-animation": OnboardingAnimation
  },
  methods: {
    checkAppMode() {
      if (window.matchMedia("(display-mode: standalone)").matches) {
        console.log("This is running as standalone/PWA.");
      } else {
        console.log("This is running on the browser");
        // this.$router.push({ path: "/" });
      }
    },
    askLocPermission() {
      // console.log(navigator.geolocation)
      if (navigator.geolocation) {
        navigator.geolocation.watchPosition(
          this.updatePosition,
          this.accesDenied
        );
        this.locationPermission = !this.locationPermission;
      } else {
        console.log("Geolocation wordt niet ondersteund door deze browser");
      }
      this.checkAllPermission();
    },
    accesDenied(error) {
      if (error.code == error.PERMISSION_DENIED)
        this.locationPermission = false;
      console.log("you denied the geolocation permission :-(");
    },
    updatePosition: function(position) {
      this.positionLa = position.coords.latitude;
      this.positionLo = position.coords.longitude;
    },
    askCamPermission() {
      this.currentConstraints = {
        video: {
          facingMode: this.currentCameraOption,
          width: this.rearCamResolution.width,
          height: this.rearCamResolution.height
        },
        audio: false
      };

      let curScope = this;
      navigator.mediaDevices
        .getUserMedia(this.currentConstraints)
        .then(() => {
          console.log("Permission accepted");
          curScope.camPermission = !curScope.camPermission;
        })
        .then(() => {
          curScope.checkAllPermission();
        })
        .catch(function(err) {
          console.log("==> Error occured in 'showStream':/ Permission dennied");
          console.error(err);
        });
    },
    checkAppOrientation() {
      if (window.innerWidth > window.innerHeight) {
        // you're in landscape mode
        console.log("orientation = landscape");
        this.landscapeOrientation = !this.landscapeOrientation;
      } else {
        //Check item not complete
        console.log("orientation = !landscape");
        this.landscapeOrientation = false;
      }
      this.checkAllPermission();
    },
    checkAllPermission() {
      if (
        this.locationPermission &&
        this.camPermission &&
        this.landscapeOrientation
      ) {
        this.$router.push({ path: "/client" });
      }
    }
  },
  mounted() {
    this.checkAppMode();
    this.checkAppOrientation();
    /* TO DO : SEND LOCATION COORDINATES TO STREAMING CLIENT */
  }
};
</script>

<style scoped>
.odk-title {
  font-size: 1.5rem;
  font-weight: 700;
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
  width: 20rem;
}

#cto-button {
  background: var(--yellow-color);
  color: var(--second-purple-color);
  font-family: "Open Sans", sans-serif;
  font-size: 1rem;
  font-weight: 600; /*semi- bold */
  line-height: 22px;
  width: 16rem;
  height: 2.625rem;
}

#cto-button:hover {
  background: rgba(246, 211, 101, 0.7) !important;
}

#gitlab-button {
  width: 18rem;
  height: 2.625rem;
  color: var(--second-purple-color) !important;
  border: 2px solid var(--second-purple-color) !important;
  font-family: "Open Sans", sans-serif !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  display: flex;
  align-items: center;
}

.check-item-complete {
  background: rgba(105, 89, 133, 0.6);
}

.check-icon {
  position: absolute;
  left: 0.75rem;
}

#container {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 50%;
  justify-content: center;
  align-items: center;
  background: var(--second-white-color);
  max-height: 500px;
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  top: 3rem;
}

#text-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
}

#header-section {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 15%;
  width: 100%;
  text-align: left;
}

#buttons-section {
  height: 35%;
  width: 100%;
  display: flex;
  margin-bottom: 2rem;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}

#add-to-home {
  font-weight: 700;
}

#image-section {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

#intro-img {
  max-height: 320px;
  object-fit: cover;
  /* position: relative;
  right: 2rem; */
}

@media (max-width: 1024px) and (orientation: portrait) {
  #container {
    background: var(--second-white-color);
    width: 100%;
    height: 100%;
    top: 0;
  }

  #image-section {
    display: flex;
    justify-content: flex-start;
  }
}

@media (max-width: 1024px) and (orientation: landscape) {
  #container {
    flex-direction: row;
    top: 0;
    height: 100%;
    max-width: none;
    max-height: none;
  }

  #header-section {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 10%;
    width: 100%;
    text-align: left;
  }

  #buttons-section {
    height: 50%;
    width: 100%;
    margin-bottom: 0.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
  }
}
</style>