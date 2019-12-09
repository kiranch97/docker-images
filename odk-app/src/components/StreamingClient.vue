<template>
  <div>
    <div class="video-stream">
      <video id="video" autoplay="true"></video>
      <canvas style="display: none;" id="canvas"></canvas>
    </div>
    <div class="container-grid">
      <div class="item-1">
        <div class="stream-toggle-settings">
          <b-switch
            v-model="isSwitched"
            class="stream-switch"
            size="is-large"
          ></b-switch>
          <!-- <img
            v-if="cameraFlipped"
            class="stream-flip"
            src="../assets/flip.png"
          /> -->
          <!-- @click="flipCamera()" -->
        </div>
        <div class="stream-start-settings">
          <button
            v-show="isSwitched"
            v-if="recordToggle"
            @click="startStream()"
            class="play-pause-circle"
          >
            <div class="inner-circle"></div>
          </button>
          <button v-else @click="pauseStream()" class="pause-box">
            <div class="inner-button"></div>
          </button>
        </div>
        <div class="stream-frames-settings">
          <canvas v-show="isSwitched" id="stream-canvas"></canvas>
          <img v-show="isSwitched" id="stream-frame" :src="analysedFrame" />
        </div>
      </div>
      <div class="item-2"></div>
      <div class="item-3">
        <p
          v-show="streamStatusToggle"
          id="stream-status"
          v-bind:class="{
            streamstatus: streamStatusToggle,
            streamstatuspaused: streamStatusTogglePause
          }"
        >
          Streaming
        </p>
        <stream-time
          v-show="toggleTimer"
          class="stream-timer"
          ref="streamtimer"
        ></stream-time>
      </div>
      <div class="item-4">    
          <stream-count></stream-count>   
      </div>
    </div>
  </div>
</template>
<script>
import StreamDetails from "./StreamDetails";
import StreamTime from "./StreamTime";
import StreamCount from "./StreamCount";
import { eventBus } from "../main";

export default {
  //// example from: https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Taking_still_photos
  //// https://medium.com/tsftech/using-web-sockets-to-update-images-8c66327f39a3

  name: "streaming-client",
  // ----

  // ----

  data: function() {
    return {
      apiWebsocketUrl: process.env.VUE_APP_API_WS_URL,
      debug: false,
      //UI properties
      recordToggle: true,
      streamStatusToggle: false,
      streamStatusTogglePause: false,
      toggleTimer: false,
      isSwitched: true,
      cameraFlipped: true,

      // ---- settings ----
      SETTINGS: {
        WIDTH: 1400,
        HEIGHT: 0,
        TAKE_PICTURE_EVERY_MS: 300
        // _URL: "wss://odk-video.stadswerken.amsterdam/stream"
      },
      // ---- end settings ----
      // ---- STREAM PROPERTIES ----
      streaming: false,
      width: null,
      height: null,
      video: null,
      canvas: null,
      photo: null,
      websocketConnection: null,
      intervalHandler: null,
      // ---- STREAM CONSTRAITS ----
      constraints: {
        video: {
          facingMode: {
            exact: "environment"
          },
          width: 1280,
          height: 720
        },

        audio: false
      },

      // ---- image files properties
      positionLa: null,
      positionLo: null,
      timeFormat: null,
      todayDate: null,
      appId: null,
      streamTime: "00:00:00",
      analysedFrame: null,
    };
  },

  // ==== Components ====

  components: {
    "stream-details": StreamDetails,
    "stream-time": StreamTime,
    "stream-count": StreamCount
    // "device-login": DeviceLogin
  },

  // ----

  computed: {},

  // ==== methods ====

  methods: {
    setup: function() {
      // console.log("OdkClient init!");
      this.video = document.getElementById("video");
      this.canvas = document.getElementById("canvas");
      this.photo = document.getElementById("photo");

      //Setup connection with WebSocket API
      this.setupWebSockets();
    },

    // ----

    startStream: function() {
      //change circle to pause button when stream starts
      this.recordToggle = false;

      this.cameraFlipped = false;

      // Show the Streaming status text and timer
      this.streamStatusToggle = true;
      this.toggleTimer = true;
      this.$refs.streamtimer.start();
      this.streamStatusTogglePause = false;
      document.getElementById("stream-status").innerHTML = "Streaming";
      this.startTimeTrigger();
    },

    // ----

    startTimeTrigger: function() {
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

      //Send data to websocket API
      let data = {
        img: base64Img,
        app_id: this.appId,
        lng: this.positionLo,
        lat: this.positionLa,
        timestamp: this.timeFormat,
        state: true
      };

      // console.log('Sending data through websocket: ' + data.timestamp)

      this.websocketConnection.send(JSON.stringify(data));
    },

    // ----

    showStream() {
      let video = this.video;
      let streaming = this.streaming;

      let constraints = this.debug ? {video: true} : this.constraints

      navigator.mediaDevices
        .getUserMedia(constraints)
        .then(function(stream) {
          video.srcObject = stream;
          video.play();
        })
        .catch(function(err) {
          console.log("An error occurred: ");
          console.log(err);
        });

      //Asks User for location permission
      if (navigator.geolocation) {
        navigator.geolocation.watchPosition(this.updatePosition);
      } else {
        locationNode.innerHTML =
          "Geolocation wordt niet ondersteund door deze browser";
      }

      video.addEventListener("canplay", this.onStartedStream, false);
    },

    // ----

    pauseStream: function() {
      clearInterval(this.intervalHandler);

      //change pause to circle button when stream stops
      this.recordToggle = true;

      this.cameraFlipped = true;

      // show Stream paused text and keep showing timer
      this.streamStatusToggle = false;
      this.$refs.streamtimer.stop();
      document.getElementById("stream-status").innerHTML = "Stream Paused";
      this.streamStatusToggle = true;
      this.streamStatusTogglePause = true;
      this.toggleTimer = true;

      console.log("Stream is stopped");
      let data = {
        app_id: this.appId,
        lng: this.positionLo,
        lat: this.positionLa,
        timestamp: this.timeFormat,
        img: "None",
        state: false
      };
      let payload = data;
      this.websocketConnection.send(JSON.stringify(payload));
    },


    // ----

    updatePosition: function(position) {
      this.positionLa = position.coords.latitude;
      this.positionLo = position.coords.longitude;
    },

    // ----

    onStartedStream: function(ev) {
      // resize video
      console.log("=> onStartedStream");

      if (!this.streaming) {
        this.width = this.SETTINGS.WIDTH;
        this.height =
          this.video.videoHeight / (this.video.videoWidth / this.width);

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
      context.fillRect(0, 0, canvas.width, canvas.height);

      let data = canvas.toDataURL("image/jpeg");
      this.photo.setAttribute("src", data);
    },

    // ----

    setupWebSockets: function() {
      let websocketUrl = this.apiWebsocketUrl + '/stream'

      this.websocketConnection = new WebSocket(websocketUrl);
      this.websocketConnection.onmessage = this.receiveWebSocketsMsg;
    },

    // ----

    receiveWebSocketsMsg: function(e) {
      console.log('Websocket connection initialized')
      console.log(e);
    },

    // ----

    formatDate: function(date) {
      let year = date.getFullYear();
      let month = this.addZero(date.getMonth()) + 1;
      let day = this.addZero(date.getDate());
      let hour = this.addZero(date.getHours());
      let min = this.addZero(date.getMinutes());
      let sec = this.addZero(date.getSeconds());
      let millisec = this.addZeroMillisec(date.getMilliseconds());

      this.timeFormat =
        year +
        "-" +
        month +
        "-" +
        day +
        " " +
        hour +
        ":" +
        min +
        ":" +
        sec +
        "." +
        millisec;

      return this.timeFormat;
    },

    // ----

    todayDateFunc: function(date) {
      let year = date.getFullYear();
      let month = this.addZero(date.getMonth()) + 1;
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
        localStorage.appId == null
      ) {
        this.$router.push("/login");
        console.log("working!!");
      }
    },

    // flipCamera: function() {
    //   let video = this.video;
    //   //Pause the stream
    //   navigator.mediaDevices
    //     .getUserMedia(this.constraints)
    //     .then(function(stream) {
    //       video.srcObject = stream;
    //       video.pause();
    //       console.log("stream is stopped");
    //     })
    //     .catch(function(err) {
    //       console.log("An error occurred: ");
    //       console.log(err);
    //     });

    //   //Change camera facingMode
    //   this.constraints.video.facingMode.exact = "environment";
    //   this.showStream();
    //   console.log("camera is flipped")
    // },
  },

  // ---- On mount hook ----\\

  mounted: function() {
    let cameraOption = process.env.VUE_APP_CAMERA_OPTION
    console.log("Camera option set to: " + cameraOption)
    if (cameraOption) {
      this.constraints.video.facingMode.exact = cameraOption
    }

    // init
    this.setup();
    this.showStream();
    this.appId = localStorage.appId;
    this.checkIdNull();
    eventBus.$on("frameReceived", analysedFrame => {
      this.analysedFrame = analysedFrame;
    });
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

.container-grid {
  display: grid;
  grid-template-rows: 1fr;
  grid-template-columns: 40% 1fr 15%;
  width: 100vw;
  height: 100vh;
  position: absolute;
  overflow: hidden;
}

.item-1 {
  display: grid;
  grid-template-rows: 40% 20% 40%;
  padding: 0.9375rem; /* 15px */
}

.stream-toggle-settings {
  display: flex;
  justify-content: space-between;
  align-content: center;
}

.stream-switch {
  justify-self: center;
  align-self: start;
  transform: rotate(180deg);
}

.stream-flip {
  width: 1.5rem;
  height: 0.9969375rem;
  transform: rotate(90deg);
  margin-top: 0.625rem;
}

.stream-start-settings {
  display: flex;
  align-items: center;
}

.play-pause-circle {
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  border: 2px solid white;
  background: none;
  transition: all 0.5s;
  display: flex;
  justify-content: center;
}

.inner-circle {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: white;
  transition: all 0.5s;
}

.inner-button {
  width: 2rem;
  height: 2rem;
  border-radius: 20%;
  background: white;
  transition: all 0.5s;
  background: #db1f48;
}

.pause-box {
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  border: 2px solid white;
  background: none;
  transition: all 0.5s;
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: center;
}

.stream-frames-settings {
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.item-3 {
  justify-content: center;
  display: grid;
  grid-template-rows: 1fr 1fr;
  padding: 1.875rem;
}

.streamstatus {
  align-self: start;
  margin-top: 3rem;
  transform: rotate(90deg);
  font-size: 18px;
  color: #db1f48;
  justify-self: center;
  width: 8.125rem;
  /* text-shadow: 1px 1px 5px #000; */
}

.streamstatus::before {
  content: "";
  width: 15px;
  height: 15px;
  background: url("../assets/dot.png");
  background-repeat: no-repeat;
  position: absolute;
  top: 0.5rem;
  left: 0.5rem;
  -webkit-animation: blink 1.5s infinite both;
  animation: blink 1.5s infinite both;
}

.streamstatuspaused {
  align-self: start;
  margin-top: 3rem;
  transform: rotate(90deg);
  color: white;
  font-size: 18px;
  justify-self: center;
  width: 8.125rem;
  /* text-shadow: 1px 1px 5px #000; */
}

.streamstatuspaused::before {
  content: "";
  width: 15px;
  height: 15px;
  background: url("../assets/pause.png");
  background-repeat: no-repeat;
  position: absolute;
  top: 0.5rem;
  left: -1rem;
}

.stream-timer {
  transform: rotate(90deg);
  justify-self: center;
  align-self: end;
  color: white;
  font-size: 18px;
  text-shadow: 1px 1px 5px #000;
}

.item-4 {
  grid-column-start: 1;
  grid-column-end: 4;
  height: 15vh;
  background: #3a225d;
  opacity: 0.8;
  display: grid;
  grid-template-columns: repeat(auto-fill, 80% 20%);
}

.video-stream {
  position: absolute;
  width: 100vw !important;
  height: 100vh !important;
  z-index: 0;
  overflow: hidden !important;
}

#video {
  width: 100vw !important;
  height: auto;
  position: relative;
  bottom: 0;
}

.icons {
  height: 3rem;
  width: 3rem;
}

.stream-counts {
  transform: rotate(90deg);
  color: white;
}

.total-counts {
  font-size: 2.5rem;
  color: white;
}

.count-box-one {
  display: flex;
  justify-content: space-around;
  margin-right: 2rem;
}

.count-box-two {
  align-self: center;
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

@media (max-width: 1024px) and (orientation: landscape) {
  .container-grid {
    transform: rotate(-90deg);
    transform-origin: top right;
    width: 100vh;
    height: 100vw;
    left: -100vh;
  }

  .item-4 {
    grid-column-start: 1;
    grid-column-end: 4;
    height: 15vw;
  }

  .video-stream {
    position: absolute;
    width: 100vw;
    height: 100vh;
    z-index: 0;
    overflow: hidden;
  }

  #video {
    width: 100vw !important;
    bottom: 0;
  }
}

@media (max-width: 1024px) and (orientation: portrait) {
  /* html, body{height: 100%;} */

  .video-stream {
    position: absolute;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 0;
    overflow: hidden;
  }

  #video {
    transform: rotate(90deg);
    right: 200px;
    width: auto !important;
    height: 100% !important;
  }
}
</style>
