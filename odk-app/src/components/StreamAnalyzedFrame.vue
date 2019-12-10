<template>
  <div class="stream-frames-settings">
    <canvas id="stream-canvas"></canvas>
    <img  id="stream-frame" :src="analysedFrame" />
  </div>
</template>
<script>

export default {
  data() {
    return {
      analysedFrame: null,
      frameFetchRate: 1000,
      apiHttpUrl: process.env.VUE_APP_API_HTTP_URL
    };
  },

  methods: {
    fetchAnalysedFrames() {
      let frameEndpointBase =
        this.apiHttpUrl + "/last_analysed_frames?app_id={{APP_ID}}";

      let frameEndpoint = frameEndpointBase.replace("{{APP_ID}}", this.appId);

      fetch(frameEndpoint, {
        method: "GET",
        headers: this.requestHeaders
      })
        .then(response => {
          return response.json();
        })
        .then(results => {
          if (results.length == 0) return;

          this.analysedFrame = results.take_frame.img;

          let c = document.getElementById("stream-canvas");
          let ctx = c.getContext("2d");

          ctx.clearRect(0, 0, c.width, c.height);
          this.frameMeta = results.frame_meta;
          // loop for all boxes
          results.detected_objects.forEach(element => {
            let curScope = this;
            let cord1 = element.bbox.coordinate1;
            let cord2 = element.bbox.coordinate2;

            curScope.drawBox(cord1, cord2, curScope.frameMeta);
          });
        })
        .catch(er => {
          console.log("==> Error occured in 'fetchAnalysedFrames':" + er);
        });
    },

    drawBox(cord1, cord2, frameMeta) {
      let c = document.getElementById("stream-canvas");
      let ctx = c.getContext("2d");

      var width = frameMeta.width;
      var height = frameMeta.height;

      var canvas_width = c.width;
      var canvas_height = c.height;

      var x1 = cord1[0];
      var y1 = cord1[1];

      var x2 = cord2[0];
      var y2 = cord2[1];

      var x1_canvas = (x1 / width) * canvas_width;
      var y1_canvas = (y1 / height) * canvas_height;

      var box_width = ((x2 - x1) / width) * canvas_width;
      var box_height = ((y2 - y1) / height) * canvas_height;

      ctx.beginPath();
      ctx.rect(x1_canvas, y1_canvas, box_width, box_height);

      ctx.lineWidth = 5;
      ctx.strokeStyle = "red";
      ctx.stroke();
    }
  },

  mounted() {
    this.appId = localStorage.appId;

    console.log(
      "=> Starting 'fetchAnalysedFrames' with 'frameFetchRate': " +
        this.frameFetchRate
    );
    setInterval(this.fetchAnalysedFrames, this.frameFetchRate);
  }
};
</script>

<style scoped>
.stream-frames-settings {
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

#stream-frame {
  height: 125px;
  width: 125px;
  background: grey;
  transform: rotate(90deg);
  position: absolute;
  z-index: 1;
}

#stream-canvas {
  transform: rotate(90deg);
  height: 125px;
  width: 125px;
  position: absolute;
  z-index: 2;
}
</style>