<template>
  <div id="container">
    <div id="video-stream">
      <video id="video" autoplay="true"></video>
      <canvas style="display: none;" id="canvas"></canvas>
    </div>

    <div id="stream-information">
      <stream-count :websocketStreamState="websocketStreamState"></stream-count>

      <div id="stream-status">
        <div id="status-box">
          <div v-if="!recordToggle" class="blink-icon"></div>
          <DefaultLoader :loading="disconnectState" id="loader" :size="spinnersize" color="white" />
          <stream-time id="stream-timer" ref="streamtimer"></stream-time>
        </div>

        <transition name="fade">
          <div id="error-prompt" v-if="disconnectState">
            <p>Geen internet verbinding</p>
          </div>
        </transition>
      </div>

      <div id="stream-controls">
        <!-- CAMERA FLIP BUTTON-->
        <div id="stream-camera-flip">
          <img
            v-if="cameraIconActive"
            class="stream-flip"
            src="../assets/flip.png"
            @click="flipCamera()"
          />
        </div>

        <div id="stream-start-settings">
          <!-- PLAY/PAUSE BUTTON -->
          <div v-if="!isAuto">
            <button v-if="recordToggle" @click="startStream()" class="play-pause-circle">
              <div class="inner-circle"></div>
            </button>
            <button v-else @click="pauseStream()" class="pause-box">
              <div class="inner-button"></div>
            </button>
          </div>
        </div>

        <!-- <div id="switch-container"> -->
          <!-- MODE SWITCH BUTTON -->
          <!-- <b-switch v-model="isAuto" class="stream-switch" size="is-large">
            <p id="auto-mode">A</p>
            <p id="manual-mode">M</p>
          </b-switch> -->
        <!-- </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import StreamTime from "./StreamTime";
import StreamCount from "./StreamCount";
import { DefaultLoader } from "vue-spinners-css";
import * as NoSleep from "nosleep.js";

export default {
  //// example from: https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Taking_still_photos
  //// https://medium.com/tsftech/using-web-sockets-to-update-images-8c66327f39a3

  name: "streaming-client",
  // ----
  data: function() {
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

      // ---- settings ----
      SETTINGS: {
        minImageWidth: 608,
        minImageHeight: 608,
        TAKE_PICTURE_EVERY_MS: process.env.VUE_APP_CAPTURE_INTERVAL
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
        OFF: "off"
      },
      hasInternetConnection: null,
      connectionRetrieved: false,
      websocketConnection: null,
      intervalHandler: null,
      // ---- CAMERA CONSTRAITS ----
      prefCameraOption: process.env.VUE_APP_DEFAULT_CAMERA_OPTION, // 'environment' or 'user'
      currentCameraOption: null,
      rearCamResolution: {
        width: 1280,
        height: 720
      },
      currentConstraints: null,
      currentStream: null,

      // ---- image files properties
      positionLa: null,
      positionLo: null,
      deviceSpeed: null,
      timeFormat: null,
      todayDate: null,
      appId: null,
      userType: null,
      streamTime: "00:00:00"
    };
  },

  // ==== Components ====

  components: {
    // "stream-details": StreamDetails,
    "stream-time": StreamTime,
    "stream-count": StreamCount,
    DefaultLoader
    // "stream-analyzer": StreamAnalyzedFrame
    // "device-login": DeviceLogin
  },

  // ----

  computed: {
    combined() {
      //Cache geolocation with computed properties
      let currentLocation = {
        lo: this.positionLo,
        la: this.positionLa
      };
      return currentLocation;
    }
  },

  // ----

  watch: {
    //watching the computed combined.currentLocation property
    // combined(newValue) {
    //   console.log("GPS position changed");
    //   console.log(newValue);
    //   setTimeout(()=> {
    //     if(this.deviceSpeed == null || 0 && this.isAuto){
    //       console.log("Hold Streaming")
    //     }
    //   },3000)
    // }
  },

  // ==== methods ====

  methods: {
    setup: function() {
      //Check User_Type . If "waste_department" -> Automode, if testuser -> Manual mode
      localStorage.userType === "waste_department"
        ? (this.isAuto = true)
        : (this.isAuto = false);

      //Initialize noSleep object constructor
      this.noSleep = new NoSleep();

      // set current camera orientation
      this.currentCameraOption = this.prefCameraOption;
      this.video = document.getElementById("video");
      this.canvas = document.getElementById("canvas");
      this.photo = document.getElementById("photo");
    },

    // ----

    startStream: function() {
      //ADD SCREENLOCK ACTIVATION WHILE STREAMING
      this.noSleep.enable();
      //Setup connection with Websocket server
      this.setupWebSockets();
      //Change circle to pause button when stream starts
      this.recordToggle = false;
      //Hide camera flip so user can switch orientation while streaming
      this.cameraIconActive = false;
      //$refs is used when calling functions from child components (In this case to start the timer function)
      this.$refs.streamtimer.start();
      //document.getElementById("stream-status").innerHTML = "Streaming";
      this.startTimeTrigger();
    },

    // ----

    startTimeTrigger: function() {
      //Interval function to take screenshots of Video stream canvas
      this.intervalHandler = setInterval(
        this.takePicture,
        this.SETTINGS.TAKE_PICTURE_EVERY_MS
      );
    },

    // ----

    takePicture: function() {
      let context = this.canvas.getContext("2d");
      if (this.width && this.height) {
        this.canvas.width = this.width;
        this.canvas.height = this.height;
        context.drawImage(this.video, 0, 0, this.width, this.height);

        let img = this.canvas.toDataURL("image/jpeg");

        this.sendImage(img);
      } else {
        this.clearPhoto();
      }
    },

    // ----

    sendImage: function(base64Img) {
      this.formatDate(new Date());
      this.appId = localStorage.appId;
      this.userType = localStorage.userType;

      //Send data to websocket API
      let data = {
        img: base64Img,
        app_id: this.appId,
        user_type: this.userType,
        lng: this.positionLo,
        lat: this.positionLa,
        timestamp: this.timeFormat
      };

      this.websocketConnection.send(JSON.stringify(data));
      // console.log(this.websocketConnection);
    },

    // ----

    showStream() {
      let video = this.video;

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
        .then(function(stream) {
          curScope.currentStream = stream;
          video.srcObject = stream;
          video.play();
          console.log(`==> Stream has started with ${curScope.rearCamResolution.width} x ${curScope.rearCamResolution.height} resolution `);
          
        })
        .catch(function(err) {
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

    // ----

    pauseStream: function() {
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
        clearInterval(this.intervalHandler);
        console.log("connection Closed");
        //Change pause to circle button when stream stops
        this.recordToggle = true;
        //Show camera flip icon to user when video stream is paused
        this.cameraIconActive = true;
        this.$refs.streamtimer.reset();
      }
    },

    // ----

    holdStream() {
      if (
        this.websocketConnection.readyState === this.websocketConnection.OPEN
      ) {
        clearInterval(this.intervalHandler);
        console.log("No messages sent anymore");
        this.$refs.streamtimer.stop();
      }
    },

    // ----

    updatePosition: function(position) {
      this.positionLa = position.coords.latitude;
      this.positionLo = position.coords.longitude;
      this.deviceSpeed = position.coords.speed;
      // console.log("Speed: " + position.coords.speed)
    },

    // ----

    onStartedStream: function() {
      // resize video
      if (!this.streaming) {
        // this.width = this.SETTINGS.minImageWidth;
        // this.height = this.video.videoHeight / (this.video.videoWidth / this.width);

        this.height = this.SETTINGS.minImageHeight;
        this.width =
          (this.video.videoWidth / this.video.videoHeight) * this.height;

        // console.log("VIDEO W: " + this.video.videoWidth);
        // console.log("VIDEO H: " + this.video.videoHeight);

        // console.log("IMAGE W: " + this.width);
        // console.log("IMAGE H: " + this.height);

        this.video.setAttribute("width", this.width);
        this.video.setAttribute("height", this.height);
        this.canvas.setAttribute("width", this.width);
        this.canvas.setAttribute("height", this.height);

        this.streaming = true;
      }
    },

    // ----

    clearPhoto: function() {
      let context = this.canvas.getContext("2d");
      context.fillStyle = "#AAA";
      context.fillRect(0, 0, this.canvas.width, this.canvas.height);

      let data = this.canvas.toDataURL("image/jpeg");
      this.photo.setAttribute("src", data);
    },

    // ----

    setupWebSockets: function() {
      //Setup connection with Websocket server URL:PORT/ENDPOINT
      let websocketUrl = this.apiWebsocketUrl + "/stream";
      this.websocketConnection = new WebSocket(websocketUrl);
      // //Set websocket stream state to "on"
      this.websocketStreamState = this.streamState.ON;
      //Websocket events
      this.websocketConnection.onmessage = this.receiveWebSocketsMsg;
      this.websocketConnection.onopen = this.receiveWebSocketsMsgOnOpen;
      this.websocketConnection.onclose = this.receiveWebSocketsMsgOnClose;
    },

    // ----

    receiveWebSocketsMsg: function(e) {
      //Websocket event when Message sent by the server
      console.log("Websocket connection initialized");
      console.log(e.data);
    },

    // ----

    receiveWebSocketsMsgOnOpen: function() {
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
        document.getElementById("status-box").style.background =
          "rgba(76, 71, 85, 0.8)";
      }

      // console.log(e);
    },

    // ----

    receiveWebSocketsMsgOnClose: function() {
      //Set Play/Pause button to inital state
      this.recordToggle = true;
      this.$refs.streamtimer.reset();
      //Retry to make setup Websocket connection every 5 seconds
      if (this.websocketStreamState === this.streamState.OFF) {
        this.disconnectState = false;
      } else {
        this.websocketConnection = null;
        this.disconnectState = true;
        document.getElementById("status-box").style.background = "#c83737";
        setTimeout(this.setupWebSockets, 5000);
      }
    },

    // ----

    formatDate: function(date) {
      let year = date.getFullYear();
      let month = this.addZero(date.getMonth() + 1);
      let day = this.addZero(date.getDate());
      let hour = this.addZero(date.getHours());
      let min = this.addZero(date.getMinutes());
      let sec = this.addZero(date.getSeconds());
      let millisec = this.addZeroMillisec(date.getMilliseconds());

      this.timeFormat = `${year}-${month}-${day} ${hour}:${min}:${sec}.${millisec}`;

      return this.timeFormat;
    },

    // ----

    todayDateFunc: function(date) {
      let year = date.getFullYear();
      let month = this.addZero(date.getMonth() + 1);
      let day = this.addZero(date.getDate());

      this.todayDate = year + "-" + month + "-" + day;

      return this.todayDate;
    },

    // ----

    addZero: function(i) {
      if (i < 10) {
        i = "0" + i;
      }
      return i;
    },

    // ----

    addZeroMillisec: function(i) {
      if (i < 100) {
        i = "00" + i;
      } else if (i >= 100 < 1000) {
        i = "0" + i;
      }
      return i;
    },

    // ----

    checkIdNull: function() {
      if (
        typeof localStorage.appId == "undefined" ||
        localStorage.appId == null ||
        !localStorage.userType
      ) {
        this.$router.push("/recommendation");
      }
    },

    stopMediaTracks: function(stream) {
      stream.getTracks().forEach(track => {
        track.stop();
      });
    },

    flipCamera: function() {
      if (this.currentCameraOption == "user") {
        this.currentCameraOption = "environment";
      } else {
        this.currentCameraOption = "user";
      }
      console.log("=> Camera option changed to: " + this.currentCameraOption);

      this.stopMediaTracks(this.currentStream);
      this.showStream();
    }
  },

  mounted: function() {
    //Init
    console.log("=> Streaming Client init:");
    this.setup();
    this.showStream();

    //Retrieve localstorage appID and userType
    this.appId = localStorage.appId;
    this.userType = localStorage.userType;

    //IF USER DOENST HAVE ID REDIRECT THEM TO PWA START PAGE
    this.checkIdNull();

    console.log("Capture rate set to: " + this.SETTINGS.TAKE_PICTURE_EVERY_MS);

  }
};
</script>

<style scoped>
:root {
  font-size: 16px;
}

body {
  overflow: hidden;
}

* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

#container {
  position: relative;
  width: 100vw;
  height: 100vh;
  max-width: 896px;
  max-height: 414px;
  margin: 0 auto;
  overflow: hidden;
  display: flex;
  align-items: center;
}

#video-stream {
  position: relative;
  width: 100%;
}

#video {
  width: 100%;
  height: auto;
}

#stream-information {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
}

#stream-results {
  width: 20%;
  height: 100vh;
  padding-left: 33.891px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}

#stream-status {
  width: 60%;
  height: 100vh;
  display: flex;
  justify-content: center;
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
}

#error-prompt {
  position: absolute;
  width: 14rem;
  height: 2.5rem;
  background: var(--white-color);
  font-weight: 600;
  top: 4.5rem;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
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

#stream-controls {
  width: 20%;
  height: 100%;
  max-height: 426px;
  display: flex;
  flex-direction: column-reverse;
}

#stream-camera-flip {
  height: 30%;
  padding-right: 33.891px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

#stream-start-settings {
  position: relative;
  height: 40%;
  right: 20px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

#switch-container {
  height: 30%;
}

.stream-switch {
  position: absolute;
  right: 0.5rem;
  bottom: 2rem;
  transition: 0.5 all;
  transform: rotate(90deg);
}

#manual-mode {
  position: absolute;
  color: var(--main-purple-color);
  font-size: 1rem;
  font-weight: 600;
  left: 10.5px;
  bottom: 7px;
  transform: rotate(-90deg);
}

#loader {
  position: absolute;
  width: 18px;
  height: 18px;
  left: 0.7rem;
}

#auto-mode {
  position: absolute;
  color: var(--main-purple-color);
  font-size: 1rem;
  font-weight: 600;
  left: 24px;
  right: 0.6rem;
  bottom: 7px;
  transform: rotate(-90deg);
}

/deep/ .switch input[type="checkbox"]:checked + .check {
  background: rgba(255, 255, 255, 0.6) !important;
}

/deep/ .switch input[type="checkbox"]:focus:checked + .check {
  box-shadow: none;
}

.stream-flip {
  width: 1.5rem;
  height: 0.9969375rem;
}

.play-pause-circle {
  width: 3.2rem;
  height: 3.2rem;
  background: none;
  border: 4px solid white;
  border-radius: 50%;
  outline: none;
  transition: all 0.5s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.inner-circle {
  width: 2rem;
  height: 2rem;
  background: var(--white-color);
  border-radius: 50%;
  outline: none;
  opacity: 0.5;
  transition: all 0.5s;
}

.inner-button {
  width: 1.5rem;
  height: 1.5rem;
  background: #db1f48;
  border-radius: 20%;
  transition: all 0.5s;
}

.pause-box {
  width: 3.2rem;
  height: 3.2rem;
  background: none;
  outline: none;
  border: 4px solid white;
  border-radius: 50%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.5s;
  z-index: 2;
}

.blink-icon {
  position: absolute;
  width: 0.6rem;
  height: 0.6rem;
  background: var(--error-color);
  left: 1.3rem;
  box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.6);
  border-radius: 50%;
  -webkit-animation: blink 1.5s infinite both;
  animation: blink 1.5s infinite both;
  z-index: 10;
}

#stream-timer {
  color: var(--white-color);
  font-size: 16px;
  font-weight: 600;
  text-shadow: 0px 2px 3px rgba(0, 0, 0, 0.6);
}

.icons {
  width: 3rem;
  height: 3rem;
}

.stream-counts {
  color: var(--white-color);
  transform: rotate(90deg);
}

video {
  max-width: none !important;
}

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
