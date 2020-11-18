<template>
  <div class="container">
    <div class="stream">
      <video id="video" class="stream-video" autoplay="true" />
      <canvas id="canvas" style="display: none;" />
    </div>

    <div class="hud">
      <stream-count
        class="hud-streamresults"
        :websocket-stream-state="websocketStreamState"
      />

      <div class="hud-streamstatus">
        <div id="status-box" :class="{ 'is-recording': !recordToggle }">
          <div v-if="!recordToggle" class="blink-icon" />
          <DefaultLoader
            id="loader"
            :loading="disconnectState"
            :size="spinnersize"
            color="white"
          />
          <stream-time
            ref="streamtimer"
            class="streamtimer"
          />
        </div>
        <transition name="fade">
          <div v-if="disconnectState" id="error-prompt">
            <p>Geen internet verbinding</p>
          </div>
        </transition>
      </div>

      <div class="hud-streamcontrols">
        <!-- TOGGLE MENU BUTTON -->
        <div id="toggle-sidebar">
          <img 
            svg-inline
            src="@/assets/ui/burger-menu.svg"
            alt="Backspace"
            @click="showSidebar()"
          >
        </div>

        <!-- PLAY/PAUSE BUTTON -->
        <div id="stream-start-settings">
          <div v-if="!isAuto">
            <button
              v-if="!disconnectState && recordToggle"
              class="play-pause-circle"
              @click="startStream"
            >
              <div class="inner-circle" />
            </button>
            <button
              v-else
              class="pause-box"
              @click="pauseStream"
            >
              <div class="inner-button" />
            </button>
          </div>
        </div>

        <!-- CAMERA FLIP BUTTON-->
        <div id="stream-camera-flip">
          <svg
            v-if="cameraIconActive"
            class="stream-flip"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            @click="flipCamera()"
          >
            <path fill="#fff" fill-rule="evenodfd" d="M14.571 5.33c.71 0 1.286.576 1.286 1.286v.047h3.214c1.066 0 1.929.864 1.929 1.929v8.143a1.928 1.928 0 01-1.929 1.928H4.93A1.928 1.928 0 013 16.735V8.592c0-1.065.863-1.929 1.929-1.929h3.213v-.047c0-.71.576-1.286 1.287-1.286h5.142zm-4.315 3.899a4.004 4.004 0 00-1.857 5.342l.002.003c.014.028.03.054.045.083l-.06 2.107a.413.413 0 00.401.426H8.8a.414.414 0 00.413-.402l.03-1.064a3.988 3.988 0 004.499.704 3.969 3.969 0 002.035-2.287 3.963 3.963 0 00-.042-2.735l.158-2.116a.414.414 0 00-.826-.062l-.071.957a4.005 4.005 0 00-4.74-.956zm4.318 1.753l-1.42-.106a.415.415 0 00-.061.826l1.918.143c.216.656.215 1.36-.016 2.025-.278.8-.85 1.444-1.613 1.813-.763.37-1.623.42-2.424.141a3.146 3.146 0 01-1.255-.808l1.346.038c.227.017.419-.173.426-.401a.414.414 0 00-.402-.426l-1.945-.056a3.174 3.174 0 011.489-4.197 3.174 3.174 0 013.957 1.008z" />
          </svg>
        </div>

        <!-- MODE SWITCH BUTTON -->
        <!-- <div id="switch-container">
          <b-switch
            v-if="switchIconActive"
            v-model="isAuto"
            class="stream-switch"
            size="is-large"
          >
            <p id="auto-mode">A</p>
            <p id="manual-mode">M</p>
          </b-switch>
        </div> -->
      </div>

      <div id="stream-sidebar">
        <div id="stream-sidebar-header">
          <img 
            svg-inline
            src="@/assets/ui/chevron-left.svg"
            alt="Menu sluiten"
            @click="hideSidebar()"
          >
          <p>Terug</p>
        </div>

        <!-- Default options -->
        <div v-if="!showManualOptions" class="stream-sidebar-option" @click="showManual()">
          <img 
            svg-inline
            src="@/assets/ui/manual.svg"
            alt="Handleiding"
          >
          <p>Handleiding</p>
          <img 
            svg-inline
            src="@/assets/ui/chevron-right-grey.svg"
            alt="Naar handleiding"
            class="stream-sidebar-option-arrow"
          >
        </div>

        <div v-if="!showManualOptions" class="stream-sidebar-option" @click="logout()">
          <img 
            svg-inline
            src="@/assets/ui/logout.svg"
            alt="Uitloggen"
          >
          <p>Uitloggen</p>
        </div>

        <!-- Manual options -->
        <div v-if="showManualOptions" class="stream-sidebar-option" @click="toManual('reset-manual')">
          <img 
            svg-inline
            src="@/assets/ui/manual.svg"
            alt="Verwijder gegevens"
          >
          <p>Verwijder gegevens</p>
        </div>

        <div v-if="showManualOptions" class="stream-sidebar-option" @click="toManual('installation-manual')">
          <img 
            svg-inline
            src="@/assets/ui/manual.svg"
            alt="Installeer PWA"
          >
          <p>Installeer PWA</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import StreamTime from "./StreamTime";
import StreamCount from "./StreamCount";
import { DefaultLoader } from "vue-spinners-css";
import * as NoSleep from "nosleep.js";
import { v4 as uuidv4 } from "uuid";

export default {
  //// example from: https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Taking_still_photos
  //// https://medium.com/tsftech/using-web-sockets-to-update-images-8c66327f39a3

  name: "StreamingClient",

  components: {
    StreamTime,
    StreamCount,
    DefaultLoader,
  },

  props: {
    uniqueId: {
      type: String,
      default: null,
    },
  },

  data: function () {
    return {
      apiWebsocketUrl: process.env.VUE_APP_API_WS_URL,
      debug: false,
      //------UI properties
      //PLAY/PAUSE BUTTON
      recordToggle: true,
      //STREAM STATUS STATES
      disconnectState: false,
      spinnersize: 25,
      //AUTO/MANUAL MODE SWITCH
      isAuto: null,
      //FLIP CAMERA
      cameraIconActive: true,
      switchIconActive: false,
      //MANUAL SIDEAR
      showManualOptions: false,


      // ---- settings ----
      SETTINGS: {
        minImageWidth: 608,
        minImageHeight: 608,
        TAKE_PICTURE_EVERY_MS: process.env.VUE_APP_CAPTURE_INTERVAL,
      },
      // ---- end settings ----

      // ---- STREAM PROPERTIES ----
      noSleep: null,
      streaming: false,
      width: null,
      height: null,
      video: null,
      canvas: null,
      photo: null,
      websocketStreamState: null,
      streamState: {
        ON: "on",
        OFF: "off",
      },
      hasInternetConnection: null,
      connectionRetrieved: false,
      websocketConnection: null,
      intervalHandlerPicture: null,
      intervalHandlerCountRequest: null,
      countResult: null,
      // ---- CAMERA CONSTRAITS ----
      prefCameraOption: process.env.VUE_APP_DEFAULT_CAMERA_OPTION, // 'environment' or 'user'
      currentCameraOption: null,
      rearCamResolution: {
        width: 1280,
        height: 720,
      },
      currentConstraints: null,
      currentStream: null,

      // ---- image files properties
      positionLa: null,
      positionLo: null,
      deviceSpeed: null,
      timeFormat: null,
      todayDate: null,
      streamTime: "00:00:00",
    };
  },

  // ----

  computed: {
    combined () {
      //Cache geolocation with computed properties
      const currentLocation = {
        lo: this.positionLo,
        la: this.positionLa,
      };
      return currentLocation;
    },
  },

  mounted () {
    //IF USER DOENST HAVE userType REDIRECT THEM TO PWA START PAGE
    this.checkUserType();
    
    this.setup();
    this.showStream();

    //Set interval when connection is offline
    //Change stream state to OFF and close websocket connection
    //When user has access to internet again. and iniates a new websocket stream, Clear the interval
    //Check the user stream state. If user was streaming, restart stream. If not dont do anything.

    // this.websocketStreamState = this.streamState.OFF;
    // setInterval(this.checkInternetState, 3000);
  },

  methods: {
    setup: function () {
      //Check User_Type . If "waste_department" -> Automode, if testuser -> Manual mode
      // @todo Fix confusing issue with automatically switching mode depending on user type. (-RJS)
      // localStorage.userType === "waste_department"
      //   ? (this.isAuto = true)
      //   : (this.isAuto = false);
      this.isAuto = false;

      //Initialize noSleep object constructor
      this.noSleep = new NoSleep();

      // set current camera orientation
      this.currentCameraOption = this.prefCameraOption;
      this.video = document.getElementById("video");
      this.canvas = document.getElementById("canvas");
      this.photo = document.getElementById("photo");
    },

    startStream: function () {
      // Add screenlock activation while streaming.
      this.noSleep.enable();

      // Setup connection with Websocket server
      this.setupWebSockets();

      // Change circle to pause button when stream starts
      this.recordToggle = false;

      // Hide camera flip so user can't switch orientation while streaming.
      this.cameraIconActive = false;
      this.$refs.streamtimer.start();
      this.startTimeTrigger();
    },

    startTimeTrigger: function () {
      //Interval function to take screenshots of Video stream canvas
      this.intervalHandlerPicture = setInterval(
        this.takePicture,
        this.SETTINGS.TAKE_PICTURE_EVERY_MS
      );
    },

    takePicture: function () {
      const context = this.canvas.getContext("2d");
      if (this.width && this.height) {
        this.canvas.width = this.width;
        this.canvas.height = this.height;
        context.drawImage(this.video, 0, 0, this.width, this.height);

        const img = this.canvas.toDataURL("image/jpeg");

        this.sendImage(img);
      } else {
        this.clearPhoto();
      }
    },

    sendImage: function (base64Img) {
      this.timeFormat = this.$moment().format("YYYY-MM-DD HH:mm:ss.SSS");

      //Send data to websocket API
      const data = {
        img: base64Img,
        stream_id: localStorage.streamId,
        user_type: localStorage.userType,
        user_id: localStorage.userId || "demo",
        lng: this.positionLo,
        lat: this.positionLa,
        timestamp: this.timeFormat,
      };

      this.websocketConnection.send(JSON.stringify(data));
    },

    showStream () {
      const video = this.video;

      this.currentConstraints = {
        video: {
          facingMode: this.currentCameraOption,
          width: this.rearCamResolution.width,
          height: this.rearCamResolution.height,
        },
        audio: false,
      };

      const curScope = this;

      navigator.mediaDevices
        .getUserMedia(this.currentConstraints)
        .then(function (stream) {
          curScope.currentStream = stream;
          video.srcObject = stream;
          video.play();
        })
        .catch(function (err) {
          console.log("==> Error occured in 'showStream':");
          console.error(err);
        });

      video.addEventListener("canplay", this.onStartedStream, false);

      //Asks User for location permission
      if (navigator.geolocation) {
        navigator.geolocation.watchPosition(this.updatePosition);
      } else {
        var locationNode = document.getElementById("location");
        locationNode.innerHTML =
          "Geolocation wordt niet ondersteund door deze browser";
      }
    },

    pauseStream: function () {
      this.websocketStreamState = this.streamState.OFF;

      //Set websocket stream state to "off"
      //Check if websocket connection is established with server
      if (
        this.websocketConnection.readyState === this.websocketConnection.OPEN
      ) {
        //Disable screenlock when stream stops
        this.noSleep.disable();
        //Close websocket connection
        this.websocketConnection.close();
        //Clear snapshot interval
        clearInterval(this.intervalHandlerPicture);
        clearInterval(this.intervalHandlerCountRequest);
        //Change pause to circle button when stream stops
        this.recordToggle = true;
        //Show camera flip icon to user when video stream is paused
        this.cameraIconActive = true;
        this.$refs.streamtimer.reset();
      }
    },

    holdStream () {
      if (
        this.websocketConnection.readyState === this.websocketConnection.OPEN
      ) {
        clearInterval(this.intervalHandlerPicture);
        clearInterval(this.intervalHandlerCountRequest);
        this.$refs.streamtimer.stop();
      }
    },

    updatePosition: function (position) {
      this.positionLa = position.coords.latitude;
      this.positionLo = position.coords.longitude;
      this.deviceSpeed = position.coords.speed;
    },

    onStartedStream: function () {
      // resize video
      if (!this.streaming) {
        // this.width = this.SETTINGS.minImageWidth;
        // this.height = this.video.videoHeight / (this.video.videoWidth / this.width);

        this.height = this.SETTINGS.minImageHeight;
        this.width =
          (this.video.videoWidth / this.video.videoHeight) * this.height;

        this.video.setAttribute("width", this.width);
        this.video.setAttribute("height", this.height);
        this.canvas.setAttribute("width", this.width);
        this.canvas.setAttribute("height", this.height);

        this.streaming = true;
      }
    },

    clearPhoto: function () {
      const context = this.canvas.getContext("2d");
      context.fillStyle = "#AAA";
      context.fillRect(0, 0, this.canvas.width, this.canvas.height);

      const data = this.canvas.toDataURL("image/jpeg");
      this.photo.setAttribute("src", data);
    },

    setupWebSockets: function () {
      //Setup connection with Websocket server URL:PORT/ENDPOINT
      const websocketUrl = this.apiWebsocketUrl + "/stream";
      this.websocketConnection = new WebSocket(websocketUrl);
      // //Set websocket stream state to "on"
      this.websocketStreamState = this.streamState.ON;
      //Websocket events
      this.websocketConnection.onmessage = this.receiveWebSocketsMsg;
      this.websocketConnection.onopen = this.receiveWebSocketsMsgOnOpen;
      this.websocketConnection.onclose = this.receiveWebSocketsMsgOnClose;
    },

    receiveWebSocketsMsg: function (e) {
      //Websocket event when Message sent by the server
        console.log(e.data);
    },

    receiveWebSocketsMsgOnOpen: function () {
      //Websocket even when websocket connection between client and server is established
      console.log("Websocket connection Connected");

      // Play/pause stream button toggle
      // After Websocket connection is disconnected and then reconnects, restart the UI State to streaming
      if (this.websocketStreamState === this.streamState.ON) {
        //Set Play/Pause button to streaming
        this.recordToggle = false;
        //Start timer function
        this.$refs.streamtimer.start();

        this.disconnectState = false;
      }
    },

    receiveWebSocketsMsgOnClose: function () {
      //Set Play/Pause button to inital state
      this.recordToggle = true;
      this.$refs.streamtimer.reset();
      //Retry to make setup Websocket connection every 5 seconds
      if (this.websocketStreamState === this.streamState.OFF) {
        this.disconnectState = false;
      } else {
        this.websocketConnection = null;
        this.disconnectState = true;
        setTimeout(this.setupWebSockets, 5000);
      }
    },

    stopMediaTracks: function (stream) {
      stream.getTracks().forEach(track => {
        track.stop();
      });
    },

    flipCamera: function () {
      if (this.currentCameraOption == "user") {
        this.currentCameraOption = "environment";
      } else {
        this.currentCameraOption = "user";
      }
      console.log("=> Camera option changed to: " + this.currentCameraOption);

      this.stopMediaTracks(this.currentStream);
      this.showStream();
    },

    showSidebar () {
      const sidebar = document.getElementById("stream-sidebar");
      sidebar.style = "left: calc((100% / 3) * 2);";
    },

    hideSidebar () {
      const sidebar = document.getElementById("stream-sidebar");
      sidebar.style = "left: 100%;";
      this.showManualOptions = false;
    },

    showManual () {
      this.showManualOptions = true;
    },

    toManual (page) {
      this.$router.push(`/${page}`);
    },

    checkUserType () {
      // if localStorage.UserType exists (change streamId for new session)
      if (localStorage.userType) {
        localStorage.streamId = uuidv4();
      }
      // if user has no localStorage.userType (send to (first) welcome page)
      else {
        this.$router.push("/welcome");
      }
    },

    logout () {
      localStorage.clear();
      this.$router.push("/welcome");
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  position: relative;
  align-items: center;
  margin: 0 auto;
  width: 100vw;
  height: 100vh;
  overflow: hidden;

  @media (orientation: landscape) {
    max-width: 896px;
    max-height: 414px;
  }
}

.stream {
  position: relative;
  width: 100%;

  &-video {
    width: 100%;
    height: auto;
  }
}

.hud {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;

  &-streamresults {
    flex: 0 1 auto;
    width: 20%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  &-streamstatus {
    flex: 0 1 auto;
    width: 100%;
    display: flex;
    justify-content: center;
  }

  &-streamcontrols {
    flex: 0 1 auto;
    width: 20%;
    max-height: 426px;
    display: flex;
    flex-direction: column;
  }
}

#status-box {
  position: relative;
  width: 10rem;
  height: 2rem;
  background: rgba(76, 71, 85, 0.8);
  top: 1rem;
  border-radius: 30px;
  display: flex;
  justify-content: center;
  align-items: center;

  &.is-recording {
    background-color: var(--color-error);
  }
}

#error-prompt {
  display: flex;
  position: absolute;
  top: 4.5rem;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: var(--color-white);
  width: 14rem;
  height: 2.5rem;
  color: var(--color-error);

  &::before {
    position: absolute;
    top: 0;
    left: 0;
    border-top-left-radius: 6px;
    border-bottom-left-radius: 6px;
    background: var(--color-error);
    width: .5rem;
    height: 100%;
    content: "";
  }
}

.fade-enter-active {
  animation: slide-in-top 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
}

.fade-enter,
.fade-leave-to {
  animation: slide-in-top 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) reverse;
}

@keyframes slide-in-top {
  0% {
    -webkit-transform: translateY(-1000px);
    transform: translateY(-1000px);
    opacity: 0;
  }

  100% {
    -webkit-transform: translateY(0);
    transform: translateY(0);
    opacity: 1;
  }
}

#toggle-sidebar {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 30%;

  svg {
    outline: none;
  }
}

#stream-start-settings {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40%;
}

#stream-camera-flip {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 30%;
}

// #switch-container {
//   display: flex;
//   align-items: center;
//   justify-content: center;
//   height: 30%;
// }

// .stream-switch {
//   margin-right: 0;
//   transition: all 500ms;
//   transform: rotate(90deg);
// }

// #manual-mode {
//   position: absolute;
//   bottom: 7px;
//   left: 10.5px;
//   transform: rotate(-90deg);
//   color: var(--color-purple);
//   font-size: 1rem;
//   font-weight: 600;
// }

// #auto-mode {
//   position: absolute;
//   right: 0.6rem;
//   bottom: 7px;
//   left: 24px;
//   transform: rotate(-90deg);
//   color: var(--main-purple-color);
//   font-size: 1rem;
//   font-weight: 600;
// }

// .switch input[type="checkbox"]:checked + .check {
//   background: rgba(255, 255, 255, 0.6) !important;
// }

// .switch input[type="checkbox"]:focus:checked + .check {
//   box-shadow: none;
// }

#loader {
  position: absolute;
  width: 18px;
  height: 18px;
  left: 0.7rem;
}

.stream-flip {
  width: 2.25rem;
  height: 2.25rem;
}

.play-pause-circle {
  width: 3.5rem;
  height: 3.5rem;
  background: none;
  border: 5px solid white;
  border-radius: 50%;
  outline: none;
  transition: all 0.5s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.inner-circle {
  width: calc(2rem + 1px);
  height: calc(2rem + 1px);
  background: var(--color-white);
  border-radius: 50%;
  outline: none;
  transition: all 0.5s;
}

.inner-button {
  width: calc(1.5rem + 1px);
  height: calc(1.5rem + 1px);
  background: var(--color-error);
  border-radius: 20%;
  transition: all 0.5s;
}

.pause-box {
  width: 3.5rem;
  height: 3.5rem;
  background: none;
  outline: none;
  border: 5px solid white;
  border-radius: 50%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.5s;
}

.blink-icon {
  position: absolute;
  width: 0.6rem;
  height: 0.6rem;
  background: var(--color-white);
  left: 1.3rem;
  border-radius: 50%;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
  animation: blink 1.5s infinite both;
  z-index: 10;
}

.streamtimer {
  color: var(--color-white);
  font-size: 1rem;
  font-weight: 600;
  text-shadow: 0 2px 3px rgba(0, 0, 0, 0.6);
}

.icons {
  width: 3rem;
  height: 3rem;
}

.stream-counts {
  color: var(--color-white);
  transform: rotate(90deg);
}

video {
  max-width: none !important;
}

// Sidebar
#stream-sidebar {
  position: absolute;
  left: 100%;
  width: calc(100% / 3);
  height: 100%;
  background: var(--color-white);
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
  display: flex;
  flex-direction: column;
  transition: 0.5s;
  z-index: 10;

  &-header {
    height: 2rem;
    margin: 1.25rem 0;
    display: flex;
    align-items: center;

    svg {
      width: 1.25rem;
      margin: 0 0.75rem 0 1rem;
      outline: none;
    }

    p {
      margin: 0;
      font-weight: 600;
    }
  }

  .stream-sidebar-option {
    position: relative;
    height: 2.75rem;
    display: flex;
    align-items: center;

    &:active {
      background: rgb(226, 222, 233);
    }

    svg:first-of-type {
      width: 1.25rem;
      margin: 0 0.75rem 0 1rem;
      outline: none;
    }

    p {
      margin: 0;
    }

    &-arrow {
      position: absolute;
      right: 1rem;
      outline: none;
    }
  }
}
//

@-webkit-keyframes blink {
  0%,
  50%,
  100% {
    opacity: 1;
  }

  25%,
  75% {
    opacity: 0;
  }
}

@keyframes blink {
  0%,
  50%,
  100% {
    opacity: 1;
  }

  25%,
  75% {
    opacity: 0;
  }
}
</style>
