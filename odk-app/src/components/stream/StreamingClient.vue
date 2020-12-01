<template>
  <div class="container">
    <!-- Stream camera feed -->
    <div class="stream">
      <video id="video" class="stream-video" autoplay="true" />
      <canvas id="canvas" style="display: none;" />
    </div>

    <div id="hud">
      <!-- Stream counter -->
      <stream-count
        :web-socket-stream-state="webSocketStreamState"
      />

      <!-- Stream timer -->
      <stream-time
        :web-socket-disconnected="webSocketDisconnected"
        :record-toggle="recordToggle"
      />

      <!-- Stream controls -->
      <stream-controls
        :is-auto="isAuto"
        :record-toggle="recordToggle"
        :camera-icon-active="cameraIconActive"
      />

      <!-- Stream error handling -->
      <transition name="fade">
        <stream-error
          v-if="streamError"
          :stream-error-message="streamErrorMessage"
        />
      </transition>

      <!-- Stream sidebar -->
      <stream-sidebar />

      <!-- TEMP GPS -->
      <div id="temp-gps">
        <p>Lat: {{ location.lat }}</p>
        <p>Lng: {{ location.lng }}</p>
        <p>Speed: {{ location.speed }} km/h</p>
      </div>
      <!--  -->
    </div>
  </div>
</template>

<script>
import StreamCount from "./StreamCount";
import StreamControls from "./StreamControls";
import StreamTime from "./StreamTime";
import StreamError from "./StreamError";
import StreamSidebar from "./StreamSidebar";
import * as NoSleep from "nosleep.js";
import { v4 as uuidv4 } from "uuid";
import { eventBus } from "@/main";

export default {
  name: "StreamingClient",

  components: {
    StreamCount,
    StreamTime,
    StreamControls,
    StreamError,
    StreamSidebar,
  },

  data () {
    return {
      // -- ??? TODO
      photo: null,

      // -- 
      // Settings
      SETTINGS: {
        minImageWidth: 608,
        minImageHeight: 608,
        TAKE_PICTURE_EVERY_MS: process.env.VUE_APP_CAPTURE_INTERVAL,
      },
      apiWebSocketUrl: process.env.VUE_APP_API_WS_URL,

      // -- 
      // UI properties
      recordToggle: true, // play/stop button, true = not streaming
      isAuto: null, // manual/auto mode
      // switchIconActive: false, // manual/auto switch
      cameraIconActive: true, // flip camera button, true = visible
      streamError: false, // error, true = error occured
      streamErrorMessage: null, // error message
      hasNetworkConnection: navigator.onLine, // network state, true = online

      // -- 
      // Stream properties
      video: null, // camera feed
      canvas: null, // camera feed overlay to take screenshots
      width: null,
      height: null,
      currentStream: null, // camera feed livestream
      intervalSendPicture: null, // interval func
      prefCameraOption: process.env.VUE_APP_DEFAULT_CAMERA_OPTION, // "environment" or "user"
      minCamQuality: {
        width: 1280,
        height: 720,
      }, // minimum quality of image, lower quality cameras can't stream
      pausedStream: false,

      // -- 
      // WebSocket properties
      webSocketConnection: null, // WebSocket live connection
      webSocketStreamState: null, // WebSocket state of streaming
      streamState: {
        ON: "on",
        OFF: "off",
      }, // possible stream states
      webSocketDisconnected: false, // whether WebSocket connection is lost with server

      // -- 
      // GPS based properties
      location: {
        lat: null,
        lng: null,
        speed: null, // km/h (m/s * 3.6)
      },
    };
  },

  mounted () {
    // Check if the user is already logged in,
    // if so, create uuid streamId
    this.checkUserType();

    // Initial setup
    this.setup();

    // EventBus for receiving control usage
    eventBus.$on("startStreaming", () => {
      this.startStream();
    });
    eventBus.$on("stopStreaming", () => {
      this.stopStream();
    });
    eventBus.$on("flipCameraEmitted", () => {
      this.flipCamera();
    });

    //Set interval when connection is offline
    //Change stream state to OFF and close webSocket connection
    //When user has access to internet again. and iniates a new webSocket stream, Clear the interval
    //Check the user stream state. If user was streaming, restart stream. If not dont do anything.

    // this.webSocketStreamState = this.streamState.OFF;
    // setInterval(this.checkInternetState, 3000);
  },

  methods: {
    setup () {
      //Check User_Type . If "waste_department" -> Automode, if testuser -> Manual mode
      // @todo Fix confusing issue with automatically switching mode depending on user type. (-RJS)
      // localStorage.userType === "waste_department"
      //   ? (this.isAuto = true)
      //   : (this.isAuto = false);
      this.isAuto = false;

      // Initialize and activate noSleep to prevent sleep modus
      const noSleep = new NoSleep();
      noSleep.enable();

      // Set vars
      this.video = document.getElementById("video");
      this.canvas = document.getElementById("canvas");
      this.photo = document.getElementById("photo");

      // Show camera feed
      this.showCameraFeed();

      // Get and watch GPS position
      this.startLocation();

      // Add network eventlistener
      this.addNetworkEventListener();

      // Check current (initial) network connection
      this.handleNetworkStateChange();
    },

    // ----
    // Network state
    // ----

    addNetworkEventListener () {
      window.addEventListener("online", this.handleNetworkStateChange);
      window.addEventListener("offline", this.handleNetworkStateChange);
    },

    // ----

    handleNetworkStateChange () {
      // Retreive current network state
      this.hasNetworkConnection = navigator.onLine;

      // If network connection
      if (this.hasNetworkConnection) {
        // Delete error
        this.streamError = false;
        this.streamErrorMessage = null;
      }

      // If state went from online to offline while streaming
      if (this.webSocketStreamState === this.streamState.ON && !this.hasNetworkConnection) {
        // Pause stream
        this.pauseStream();

        return;
      }

      // If network connection is restored and stream was paused
      if (this.pausedStream && this.hasNetworkConnection) {
        // Try to make WebSocket connection again
        this.startStream();

        // Reset pausedStream var
        this.pausedStream = false;

        return;
      }

      // If initial state is "offline"
      if (!this.hasNetworkConnection) {
        // Set error
        const message = "Geen internetverbinding";
        this.errorHandling(message, false);

        return;
      }
    },

    // ----
    // UI funcs
    // ----

    flipCamera () {
      // Toggle between "user" and "environment"
      if (this.prefCameraOption === "user") {
        this.prefCameraOption = "environment";
      } else {
        this.prefCameraOption = "user";
      }

      // Stop current camera feed
      this.stopMediaTracks(this.currentStream);

      // Start new feed with different camera
      this.showCameraFeed();
    },

    // ----

    errorHandling (message, timeout) {
      this.streamErrorMessage = message;
      this.streamError = true;

      if (timeout) {
        setTimeout(() => {
          this.streamError = false;
          this.streamErrorMessage = null;
        }, 5000);
      }
    },

    // ----
    // Start and Stop camera feed
    // ----

    showCameraFeed () {
      // Get camera feed
      const video = this.video;

      // Create camera feed options
      const currentConstraints = {
        video: {
          facingMode: this.prefCameraOption,
          width: this.minCamQuality.width,
          height: this.minCamQuality.height,
        },
        audio: false,
      };

      const curScope = this;

      // Set camera feed options
      navigator.mediaDevices
        .getUserMedia(currentConstraints)
        .then(function (stream) {
          curScope.currentStream = stream;
          video.srcObject = stream;
          video.play();
        })
        .catch(function (err) {
          console.log("==> Error occured in 'showCameraFeed':");
          console.error(err);
        });

      video.addEventListener("canplay", this.onStartedStream, false);
    },

    // ----

    stopMediaTracks (stream) {
      // Stop every track (a/v)
      stream.getTracks().forEach(track => {
        track.stop();
      });
    },

    // ----
    // GPS based funcs
    // ----

    startLocation () {
      // Set options
      const geoOptions = {
        enableHighAccuracy: true,
      };

      // Fetch location once
      navigator.geolocation.getCurrentPosition(this.updatePosition, this.positionError, geoOptions);

      // Keep watching location
      navigator.geolocation.watchPosition(this.updatePosition, this.positionError, geoOptions);
    },

    // ----

    updatePosition (position) {
      // Set new GPS location values
      this.location.lat = position.coords.latitude;
      this.location.lng = position.coords.longitude;
      this.location.speed = position.coords.speed * 3.6 || 0; // m/s to km/h = x * 3.6
    },

    // ----

    positionError (err) {
      console.warn(`ERROR(${err.code}): ${err.message}`);
    },

    // ----
    // Start, onStart. Stop and Pause stream
    // ----

    startStream () {
      // Setup connection with WebSocket server and
      // start stream
      this.setupWebSocket();
    },

    // ----

    onStartedStream () {
      // resize video
      this.height = this.SETTINGS.minImageHeight;
      this.width = (this.video.videoWidth / this.video.videoHeight) * this.height;

      this.video.setAttribute("width", this.width);
      this.video.setAttribute("height", this.height);
      this.canvas.setAttribute("width", this.width);
      this.canvas.setAttribute("height", this.height);

      this.streaming = true;
    },

    // ----

    pauseStream () {
      // Close WebSocket connection
      this.webSocketConnection.close();

      // Stop making and sending screenshots
      clearInterval(this.intervalSendPicture);

      // Set var
      this.pausedStream = true;
      
      // Pause timer
      eventBus.$emit("pauseStreamTimer");
    },

    // ----

    stopStream () {
      // Set webSocket stream state to "off"
      this.webSocketStreamState = this.streamState.OFF;

      // Close webSocket connection
      this.webSocketConnection.close();

      // Stop making and sending screenshots
      clearInterval(this.intervalSendPicture);

      // Set Play/Stop button to inital state
      this.recordToggle = true;

      // Show camera flip icon
      this.cameraIconActive = true;

      // Reset timer
      eventBus.$emit("resetStreamTimer");
    },

    // ----
    // Interval take picture
    // ----

    startTimeTrigger () {
      // Interval function to take screenshots of Video stream canvas
      this.intervalSendPicture = setInterval(
        this.takePicture,
        this.SETTINGS.TAKE_PICTURE_EVERY_MS
      );
    },

    // ----
    // Take and Clear picture funcs
    // ----

    takePicture () {
      if (this.width && this.height) {
        // Check if vehicle is moving (minimum of 2.5km/h)
        // send image if so
        if (this.location.speed > 2.5) {
          const context = this.canvas.getContext("2d");
          this.canvas.width = this.width;
          this.canvas.height = this.height;
          context.drawImage(this.video, 0, 0, this.width, this.height);

          const screenshot = this.canvas.toDataURL("image/jpeg");
          this.sendImage(screenshot);
        } else {
          console.debug(`Not sending frame. Car is moving too slow (${this.location.speed} km/h)`);
        }
      } 
      
      else {
        // what TODO ??
        this.clearPhoto();
      }
    },

    // ----

    clearPhoto () { // what TODO ??
      const context = this.canvas.getContext("2d");
      context.fillStyle = "#AAA";
      context.fillRect(0, 0, this.canvas.width, this.canvas.height);

      const screenshot = this.canvas.toDataURL("image/jpeg");
      this.photo.setAttribute("src", screenshot);
    },

    // ----
    // WebSocket funcs
    // ----

    setupWebSocket () {
      console.debug("Try to establish WebSocket connection");

      // Setup connection with WebSocket server URL:PORT/ENDPOINT
      const webSocketUrl = this.apiWebSocketUrl + "/stream";
      this.webSocketConnection = new WebSocket(webSocketUrl);

      // WebSocket events
      this.webSocketConnection.onopen = this.receiveWebSocketMsgOnOpen;
      this.webSocketConnection.onclose = this.receiveWebSocketMsgOnClose;
      this.webSocketConnection.onmessage = this.receiveWebSocketMsg;
      this.webSocketConnection.onerror = this.receiveWebSocketMsgOnError;
    },

    // ----

    receiveWebSocketMsgOnOpen () {
      console.debug("WebSocket connection established");

      // StreamState = ON
      this.webSocketStreamState = this.streamState.ON;

      // Set Play/Stop button to streaming
      this.recordToggle = false;

      // Hide camera flip icon
      this.cameraIconActive = false;

      // Start timer
      eventBus.$emit("startStreamTimer");

      // Start taking screenshots
      this.startTimeTrigger();
    },

    // ----

    receiveWebSocketMsgOnClose () {
      console.debug("WebSocket connection closed");

      // Set Play/Stop button to inital state
      this.recordToggle = true;

      // Show camera flip icon
      this.cameraIconActive = true;

      // Reset timer
      eventBus.$emit("resetStreamTimer");

      // Delete webSocket connection
      this.webSocketConnection = null;
    },

    // ----

    receiveWebSocketMsg (e) {
      console.debug("WebSocket message received");

      // WebSocket event when Message sent by the server
      console.log(e);
      // console.log(e.data);
    },

    // ----

    receiveWebSocketMsgOnError () {
      console.debug("WebSocket connection failed to establish");

      // Set error
      const message = "Verbinding met server mislukt";
      this.errorHandling(message, true);
    },

    // ----

    sendImage (base64Img) {
      console.debug("WebSocket send message");

      // Set message to send
      const message = {
        img: base64Img,
        stream_id: localStorage.streamId,
        user_type: localStorage.userType,
        user_id: localStorage.userId || "demo",
        lat: this.location.lat,
        lng: this.location.lng,
        timestamp: this.$moment().format("YYYY-MM-DD HH:mm:ss.SSS"),
      };

      // Send message to webSocket API
      this.webSocketConnection.send(JSON.stringify(message));
    },

    // ----
    // Validation funcs
    // ----

    checkUserType () {
      // If localStorage.UserType exists (change streamId for new session)
      if (localStorage.userType) {
        // Get uuid
        const uuid = uuidv4();

        // Set localStorage
        localStorage.streamId = uuid;

        // Send new streamId to other components
        eventBus.$emit("newStreamId", uuid);
      }
      // if user has no localStorage.userType (send to (first) welcome page)
      else {
        this.$router.push("/welcome");
      }
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

#hud {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
}

video {
  max-width: none !important;
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

// TEMP GPS
#temp-gps {
  position: absolute;
  bottom: 0;
  padding: 0 1rem;
  background: #fff;
  font-size: 0.75rem;
}
// 
</style>
