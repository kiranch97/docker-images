<template>
  <div id="odk-client">
    <h3>odk-client</h3>
     <div class="camera">
        <video id="video">Video stream not available.</video>
    </div>
    <canvas id="canvas">
        <!-- canvas output -->
    </canvas>
    <div class="output">
        <img id="photo" alt="The screen capture will appear in this box.">
    </div>
  </div>
</template>

<script>


export default {

    //// example from: https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Taking_still_photos
    //// https://medium.com/tsftech/using-web-sockets-to-update-images-8c66327f39a3

  name: 'OdkClient',
  components: {
  },

  // ----

  props: [], 

  // ----

  data : function()
  { 
    return {
      // ---- settings ----      
      SETTINGS:
      {
          WIDTH: 800,
          HEIGHT: 0,
          TAKE_PICTURE_EVERY_MS : 500, // 100 = 10fps // 33 ≈ 30fps // 16 ≈ 60fps //
          WEBSOCKET_URL : "ws://localhost:8090/stream",
          // WEBSOCKET_URL : "wss://odk-video.stadswerken.amsterdam/stream",
      },
      // ---- end settings ----
      // ---- PROPERTIES ----
        streaming : false,
        width: null,
        height: null,
        video : null,
        canvas : null,
        photo : null,
        websocketConnection : null,
        intervalHandler : null,
    };
  }, 

  // ----
  
  computed : {
      
  },

  // ==== methods ====

  methods: {

    setup : function()
    {
        console.log("OdkClient init!");
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.photo = document.getElementById('photo');

        this.startStream();
        this.startTimeTrigger();

        this.setupWebSockets();
    },

    // ----

    startStream : function()
    {
        let video = this.video;
        let streaming = this.streaming;

        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        .then(function(stream) {
            video.srcObject = stream;
            video.play();
        })
        .catch(function(err) {
            console.log("An error occurred: " + err);
        });

        if (navigator.geolocation) {
        navigator.geolocation.watchPosition(this.showPosition);
      } else {
        locationNode.innerHTML =
          "Geolocation wordt niet ondersteund door deze browser";
      }

        video.addEventListener('canplay', this.onStartedStream, false);
    },


    // ----

    startTimeTrigger : function()
    {
        setInterval(this.doJob, this.SETTINGS.TAKE_PICTURE_EVERY_MS);
    },

       // ----

    showPosition : function(position) 
    {
      var locationNode = document.getElementById("location");
      locationNode.innerHTML =
        position.coords.latitude + "_" + position.coords.longitude;
    },


    // ----

    doJob : function()
    {
        console.log("=> do Job! ");
        this.takePicture();

        /*
        // TEST 
        this.sendWebSocketsMsg({"msg": "test bericht: " + new Date().toString() })
        */
    },

    // ----

    onStartedStream : function(ev)
    {
        // resize video
        
        console.log("=> onStartedStream");

        if (!this.streaming)
        {
                this.width = this.SETTINGS.WIDTH;
                this.height = this.video.videoHeight / (this.video.videoWidth/this.width);
            
                this.video.setAttribute('width', this.width);
                this.video.setAttribute('height', this.height);
                this.canvas.setAttribute('width', this.width);
                this.canvas.setAttribute('height', this.height);
                this.streaming = true;
        }
    },

    // ----

    clearphoto : function() 
    {
        let context = this.canvas.getContext('2d');
        context.fillStyle = "#AAA";
        context.fillRect(0, 0, canvas.width, canvas.height);

        let data = canvas.toDataURL('image/png');
        this.photo.setAttribute('src', data);
    },

    // ----

    takePicture : function() 
    {
        let context = this.canvas.getContext('2d');
        if (this.width && this.height)
        {
            this.canvas.width = this.width;
            this.canvas.height = this.height;
            context.drawImage(this.video, 0, 0, this.width, this.height);
            
            let img = this.canvas.toDataURL('image/png');
            // photo.setAttribute('src', data); // no needed anymore
            this.sendImage(img);
        } 
        else {
            clearphoto();
        }
    },

    setupWebSockets : function()
    {
        // setup websocket connection

        console.log("=> setupWebSockets");

        this.websocketConnection = new WebSocket(this.SETTINGS.WEBSOCKET_URL);
        this.websocketConnection.onmessage = this.receiveWebSocketsMsg;
    },

    // ----

    sendWebSocketsMsg : function(data) 
    { 
        console.log("=> Send Message:");
        console.log(data)
        let payload = data;
        this.websocketConnection.send(JSON.stringify(payload));
    },

    // ----

    receiveWebSocketsMsg : function(e)
    {
        console.log(e);
    },

    // ----

    sendImage : function(base64Img)
    {
        let data = { 
                        img : base64Img, 
                        createdAt : new Date().toString(),
                        lng: 5.3,
                        lat: 50.3,
                    }
        this.sendWebSocketsMsg(data);
    }

    // ----

  },

  // ==== 
  mounted : function() {
    // init
    this.setup();
  }
}
</script>


<style scoped>

#odk-client {
    display: block;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
    height: 90vh;
    border: 2px solid #444;
    margin-top: 20px;
    background: white;
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
}

</style>
