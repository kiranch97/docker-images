<template>
  <div>
    <div class="custom-grid">
      <div></div>
      <div></div>
      <div></div>
      <div class="box-1">
        <!-- <div></div>
        <div class="inner-box-1">
          <img id="logo" src="../assets/odk-white.png" />
        </div>
        <div></div> -->
      </div>

      <div class="box-2">
        <!-- <div class="box-2-login">
          
        </div>-->
        <!-- <div class="box-2-video">
          <keep-alive>
           
            <transition name="fade">
            <stream-details
              class="stream-details"
              v-show="popUpToggle"
              :width="width"
              :height="height"
              :imageCount="imageCount"
            ></stream-details>
            </transition>
          </keep-alive>
        
          <video id="video" autoplay="true"></video>
      
         
        </div>
        <canvas style="display: none;" id="canvas">
        
        </canvas> -->
        <!-- <div class="box-2-details">
         
        </div>-->

        <!-- <div  class="camera">
          <video id="video">Video stream not available Yet.</video>
        </div>-->

        <!-- <div style="display:none;" class="output">
          <img id="photo" alt="The screen capture will appear in this box." />
        </div> -->
      </div>

      <div class="box-3">
        <!-- <div >
        </div>
        <div class="flex">
          <button v-if="recordToggle" @click="startStream()" class="play-pause-circle">
            <div class="inner-circle"></div>
          </button>
          <button v-else @click="stopStream()" class="pause-box">
            <div class="inner-button"></div>
          </button>
        </div>
        <div class="flex-2">
          <b-button @click="change()" class="report-box">
            <b-icon class="report-icon" pack="far" icon="far fa-file-alt" size="large"></b-icon>
          </b-button>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import StreamDetails from "./StreamDetails";
// import DeviceLogin from "./DeviceLogin";

export default {
  //// example from: https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Taking_still_photos
  //// https://medium.com/tsftech/using-web-sockets-to-update-images-8c66327f39a3

  name: "ODK-PWA-Client",
  // ----

  // props: [myId],

  // ----

  data: function() {
    return {
      //UI properties
      recordToggle: true,
      popUpToggle: false,

      // ---- settings ----
      SETTINGS: {
        WIDTH: 800,
        HEIGHT: 0,
        TAKE_PICTURE_EVERY_MS: 300,
        WEBSOCKET_URL: null
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
           width: 1280,
           height: 720,
        },

        audio: false
      },
      facingMode: false,

      // ---- image files properties
      positionLa: null,
      positionLo: null,
      timeFormat: null,
      imageCount: 0,
      myId: null
    };
  },

  // ==== Components ====

  components: {
    "stream-details": StreamDetails,
    // "device-login": DeviceLogin
  },

  // ----

  computed: {},

  // ==== methods ====

  methods: {
    setup: function() {
      console.log("OdkClient init!");
      this.video = document.getElementById("video");
      this.canvas = document.getElementById("canvas");
      this.photo = document.getElementById("photo");

      //Setup connection with WebSocket API
      this.setupWebSockets();
    },

    // ----

    startStream: function() {
      let video = this.video;
      let streaming = this.streaming;

      this.recordToggle = false;

      //Asks user for Camera permission to start stream.
      navigator.mediaDevices
        .getUserMedia(this.constraints)
        .then(function(stream) {
          video.srcObject = stream; 
          video.play();
        })
        .catch(function(err) {
          console.log("An error occurred: ");
          console.log( err);
        });

     
      //Asks User for location permission
      if (navigator.geolocation) {
        navigator.geolocation.watchPosition(this.updatePosition);
      } else {
        locationNode.innerHTML = "Geolocation wordt niet ondersteund door deze browser";
      }

      video.addEventListener("canplay", this.onStartedStream, false);

      this.startTimeTrigger();
    },

    // ----

    stopStream: function() {
      clearInterval(this.intervalHandler);
      this.recordToggle = true;

      console.log("Stream is stopped");
      let data = {
        appId: this.myId,
        lng: this.positionLo,
        lat: this.positionLa,
        timestamp: this.timeFormat,
        img: false,
        state: false
      };
      let payload = data;
      this.websocketConnection.send(JSON.stringify(payload));
    },

    // ----

    startTimeTrigger: function() {
      this.intervalHandler = setInterval(
        this.doJob,
        this.SETTINGS.TAKE_PICTURE_EVERY_MS
      );
    },

    // ----

    updatePosition: function(position) {
      this.positionLa = position.coords.latitude;
      this.positionLo = position.coords.longitude;
    },

    // ----

    doJob: function() {
      // console.log("=> do Job! ");
      this.takePicture();
    },

    // ----

    onStartedStream: function(ev) {
      // resize video

      console.log("=> onStartedStream");
      
      if (!this.streaming) {
        this.width = this.SETTINGS.WIDTH;
        this.height = this.video.videoHeight / (this.video.videoWidth / this.width);
        
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

    takePicture: function() {
      let context = this.canvas.getContext("2d");
      if (this.width && this.height) {
        this.canvas.width = this.width;
        this.canvas.height = this.height;
        context.drawImage(this.video, 0, 0, this.width, this.height);

        let img = this.canvas.toDataURL("image/jpeg");
        
        this.sendImage(img);
        this.imageCount += 1;
      } else {
        this.clearPhoto();
      }
    },

    // ----

    setupWebSockets: function() {
      // setup websocket connection
      console.log("=> setupWebSockets");

      this.websocketUrlHandler();

      this.websocketConnection = new WebSocket(this.SETTINGS.WEBSOCKET_URL);
      this.websocketConnection.onmessage = this.receiveWebSocketsMsg;
    },

    // ----

    sendWebSocketsMsg: function(data) {
      // console.log("=> Send Message:");
      // console.log(data);
      let payload = data;
      this.websocketConnection.send(JSON.stringify(payload));
    },

    // ----

    receiveWebSocketsMsg: function(e) {
      console.log(e);
    },

    // ----

    sendImage: function(base64Img) {
      this.formatDate(new Date());

      this.myId = localStorage.deviceId;

      //Send data to websocket API
      let data = {
        img: base64Img,
        appId: this.myId,
        lng: this.positionLo,
        lat: this.positionLa,
        timestamp: this.timeFormat,
        state: true
      };

      this.sendWebSocketsMsg(data);
    },

    // ----

    formatDate: function(date) {
      let hour = this.addZero(date.getHours());
      let min = this.addZero(date.getMinutes());
      let sec = this.addZero(date.getSeconds());
      let millisec = this.addZeroMillisec(date.getMilliseconds());
      this.timeFormat = hour + ":" + min + ":" + sec + "." + millisec;

      return this.timeFormat;
    },

    // ----

    addZero: function(i) {
      if (i < 10) {
        i = "0" + i;
      }
      return i;
    },

    addZeroMillisec: function(i) {
      if (i < 100) {
        i = "00" + i;
      }
      else if (i >= 100 <1000) {
        i = "0" + i;
      }
      return i;
    },

    // ----

    change: function() {
      this.popUpToggle = !this.popUpToggle;
      // console.log(this.popUpToggle);
    },

    websocketUrlHandler: function() {
      if (
        location.hostname === "localhost" ||
        location.hostname === "127.0.0.1" ||
        location.hostname === ""
      ) {
        this.SETTINGS.WEBSOCKET_URL = "ws://localhost:8090/stream";
      } else {
        this.SETTINGS.WEBSOCKET_URL ="wss://odk-video.stadswerken.amsterdam/stream";
      }
    },
  },

  // ---- On mount hook ----\\

  mounted: function() {
    // init
    this.setup();
  }
};
</script>


<style scoped>

video {
  max-width: none !important;
}

body {
  margin: 0;
  font-family: soleil, sans-serif !important;
  font-style: normal;
  font-weight: 300;
  overflow: hidden;
}

h2 {
  font-size: 30px;
  color: #f4f0e6;
}

#logo {
  /* height: 2.19rem; */
  /* width: 8.7rem; */
  height: 0.876rem;
  width: 3.48rem;
}

.report-box {
  width: 30px;
  border-radius: 15%;
  border: 2px solid #242424;
  background: #e1d9d6;
}

.custom-grid {
  height: 100vh;
  width: 100vw;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr ;
  grid-template-rows: 85% 15%; 
}

.box-1 {
  background-color: #242424;
  grid-column-start: 1;
  grid-column-end: 4;
}

.inner-box-1 {
  display: flex;
  justify-content: center;
  align-items: center;
}

.box-2 {
  display: grid;
  grid-template-columns: 1fr;
  width: 100%;
  height: 100%;
  background: #eeeae0;
  /* border: blue 2px solid; */
}

.stream-details {
  position: absolute;
  z-index: 4;
  margin: 0 auto;
  bottom: 15%;
  right: 0%;
}

.device-login {
  position: absolute;
  z-index: 4;
  margin: 0 auto;
}

.box-3 {
  background-color: #242424;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
}

.flex {
  display: flex;
  height: 100%;
  justify-content: center;
  align-items: center;
}

.flex-2 {
  display: flex;
  height: 100%;
  justify-content: center;
  align-items: center;
}

.play-pause-circle {
  width: 75px;
  height: 75px;
  border-radius: 50%;
  background: grey;
  transition: all 0.5s;
  border: none;
  display: flex;
  justify-content: center;
}

button {
  all: unset;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s ease-out;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}


.inner-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: lightgrey;
  transition: all 0.5s;
  box-shadow: 1px 2px 4px rgba(0, 0, 0, 0.5);
}

.inner-circle:active {
  transform: translateY(1.5px);
}

.inner-button {
  width: 60px;
  height: 60px;
  border-radius: 20%;
  background: lightgrey;
  transition: all 0.5s;
  box-shadow: 1px 2px 4px rgba(0, 0, 0, 0.5);
}

.inner-button:active {
  transform: translateY(2px);
}

.pause-box {
  width: 75px;
  height: 75px;
  border-radius: 20%;
  background: grey;
  transition: all 0.5s;
  position: relative;
  z-index: 2;
  border: none;
  display: flex;
  justify-content: center;
}

.box-2-login {
  display: flex;
  position: relative;
  left: 128%;
  z-index: 3;
  margin: 0 auto;
  align-items: center;
}

.box-2-details {
  display: flex;
  justify-content: flex-start;
  align-items: flex-end;
}

.box-2-video {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

/* .media {
  height: 100%;
  width: 100%;
} */

#video {
  width: 100%; 
  height: 100%;
}

.slide-enter {
  opacity: 0;
}

.slide-enter-active {
  animation: slide-in 1s ease-out forwards;
  transition: opacity 0.5s;
}

.slide-leave {
}

.slide-leave-active {
  animation: slide-out 1s ease-out forwards;
  transition: opacity 0.5s;
  opacity: 0;
}


@media (max-width: 812px) and (orientation: landscape) {
  /* .custom-grid {
    transform: rotate(-90deg);
    width: 100vh;
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 10vw 75vw 15vw;
  } */

  .custom-grid {
  height: 100vh;
  width: 100vw;
  transform: rotate(-90deg);
  display: grid;
  grid-template-columns: 1fr 1fr 1fr ;
  grid-template-rows: 85% 15%; 
}

  .box2 {
    display: grid;
    grid-template-columns: 1fr;
    width: 100%;
    height: 200%;
    background: #eeeae0;
  }

  #video {
    height: 150%;
    width: 100vw;    
    transform: rotate(90deg);
    transition: all 0.2s;
  }

  .report-icon {
    transform: rotate(90deg);
    transition: all 0.2s;
  }

  #logo {
    height: 0.876rem;
    width: 3.48rem;
    transform: rotate(90deg);
    transition: all 0.2s;
  }

  .box-2-login {
    display: flex;
    position: relative;
    left: 70%;
    z-index: 3;
    margin: 0 auto;
    align-items: center;
  }

  .stream-details {
    position: absolute;
    z-index: 4;
    margin: 0 auto;
    top: 117.5%;
    right: 2%;

  }

  .device-login {
    position: absolute;
    z-index: 4;
    margin: 0 auto;
    transform: rotate(90deg);
    transition: all 0.2s;
  }
}
</style>
