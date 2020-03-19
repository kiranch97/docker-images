<template>
  <div id="container">
    <div id="image-section">
      <onboarding-animation></onboarding-animation>
    </div>
    <div id="text-section">
      <div id="header-section">
        <p class="odk-title" id="title">Voordat u begint</p>
      </div>
      <div id="buttons-section">
        <button
          :class="{ 'check-item-complete' : landscapeOrientation}"
          rounded
          id="transparent-button"
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
          <span>Houd uw telefoon liggend</span>
        </button>

        <button
          rounded
          id="loc-check-button"
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
          <span id="buttonspan">GPS-locatie inschakelen</span>
        </button>

        <button
          :class="{ 'check-item-complete' : camPermission}"
          class="camera-button"
          @click="askCamPermission()"
          id="camera-check-button"
          size="is-medium"
          disabled="true"
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
          </svg>
          <span id="buttonspan2">Camera inschakelen</span>
        </button>
      </div>
      <p class="body-1" id="tip">Als u deze stappen niet volgt, zal u ODK niet kunnen gebruiken</p>
    </div>
  </div>
</template>

<script>
import OnboardingAnimation from "./OnboardingAnimation.vue";
export default {
  name: "checklist-page",
  data() {
    return {
      ///UI properties
      landscapeOrientation: false,
      locationPermission: false,
      camPermission: false,
      //GEOLOCATION COORDINATES
      positionLa: null,
      positionLo: null,
      currentCameraOption: null,
      //FRONT CAMERA RESOLUTION
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
    //-------

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

    //-------

    askLocPermission() {
      // console.log(navigator.geolocation)
      if (navigator.geolocation) {
        navigator.geolocation.watchPosition(
          this.updatePosition,
          this.accesDenied
        );
        this.locationPermission = !this.locationPermission;
        document.getElementById("buttonspan").style.marginLeft = "0";
        document.querySelector(".camera-button").removeAttribute("disabled");
      } else {
        console.log("Geolocation wordt niet ondersteund door deze browser");
      }
      this.checkAllPermission();
    },

    //-------

    accesDenied(error) {
      if (error.code == error.PERMISSION_DENIED)
        this.locationPermission = false;
      console.log("you denied the geolocation permission :-(");
      document.getElementById("buttonspan").style.marginLeft = "1.75rem";
      document.querySelector(".camera-button").disabled = true;
    },

    //-------

    updatePosition: function(position) {
      this.positionLa = position.coords.latitude;
      this.positionLo = position.coords.longitude;
    },

    //-------

    askCamPermission() {
      this.currentConstraints = {
        video: {
          facingMode: this.currentCameraOption,
          width: this.rearCamResolution.width,
          height: this.rearCamResolution.height
        },
        audio: false
      };
      //INNER SCOPE
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

    //-------

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

    //-------

    checkAllPermission() {
      if (
        this.locationPermission &&
        this.camPermission &&
        this.landscapeOrientation
      ) {
        this.$router.push({ path: "/client" });
      }
    }

    //-------
  },
  mounted() {
    // Init
    // check if locationPermission, camPermission en landscape orientation is active
    this.checkAppMode();
    this.checkAppOrientation();

    document.getElementById("buttonspan").style.marginLeft = "1.75rem";
    document.getElementById("buttonspan2").style.marginLeft = "1.75rem";

    //TODO: IF THIS.checkAppOrientation = TRUE  then go to /client immedietly
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
  padding: 0 2rem 0 1rem;
  background: var(--second-white-color);
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

#image-section {
  width: 50%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

#intro-img {
  object-fit: cover;
}

#text-section {
  width: 50%;
  height: 100%;
  max-width: 20rem;
  padding: 2.5rem 0 2.5rem 3rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

#header-section {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  text-align: left;
  width: 100%;
}

#camera-check-button, #loc-check-button {
  width: 100%;
  font-family: "Open Sans", sans-serif;
  font-size: 1rem;
  font-weight: 600;
  text-align: center;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 30px;
  display: flex;
  justify-content: left;
  align-items: center;
}

#camera-check-button, #loc-check-button {
  background: transparent;
  color: var(--second-purple-color);
  border: 2px solid var(--second-purple-color);
  margin-top: 1rem;
}

#camera-check-button:active, #loc-check-button:active {
  background: rgba(105, 89, 133, 0.6);
}

#camera-check-button:disabled, #loc-check-button:disabled {
  background: transparent;
  color: #b8b1c3;
  border: 2px solid #ebebf2;
}

#transparent-button {
  width: 100%;
  font-family: "Open Sans", sans-serif;
  font-size: 1rem;
  font-weight: 600;
  text-align: center;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 30px;
  display: flex;
  justify-content: left;
  align-items: center;
}

#transparent-button {
  background: transparent;
  color: var(--second-purple-color);
  border: 2px solid var(--second-purple-color);
  margin-top: 1rem;
}

#transparent-button:active{
  background: rgba(105, 89, 133, 0.6);
}

#transparent-button:disabled {
  background: transparent;
  color: #b8b1c3;
  border: 2px solid #ebebf2;
}

.check-item-complete {
  background: rgba(105, 89, 133, 0.6) !important;
}

.check-icon {
  margin-right: 0.25rem;
}

#tip{
  text-align: left;
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