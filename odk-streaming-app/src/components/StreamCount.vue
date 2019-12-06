<template>
  <div class="item-4">
    <div class="count-box-one">
      <div class="stream-counts">
        <img class="icons" src="../assets/bin-icon.png" />
        <p>{{ binCount }}</p>
      </div>
      <div class="stream-counts">
        <img class="icons" src="../assets/cb-icon.png" />
        <p>{{ cardboardCount }}</p>
      </div>
      <div class="stream-counts">
        <img class="icons" src="../assets/tb-icon.png" />
        <p>{{ trashCount }}</p>
      </div>
    </div>

    <div class="stream-counts count-box-two">
      <p class="total-counts">{{ totalCount }}</p>
    </div>
  </div>
</template>
<script>
import { eventBus } from "../main";

export default {
  name: "stream-count",
  data() {
    return {
      binCount: [],
      trashCount: [],
      cardboardCount: [],
      totalCount: 0,
      appId: null,
      analysedFrame: null,
      requestHeaders: {
        "Content-Type": "application/json",
        Authorization: "No Auth"
      }
    };
  },

  methods: {
    fetchAnalysedResults: function() {
      let curEndPoint = process.env.VUE_APP_DATE_ENDPOINT.replace(
        "{{APP_ID}}",
        this.appId
      ).replace("{{DATE}}", this.todayDateFunc(new Date()));

      fetch(curEndPoint, {
        method: "GET",
        headers: this.requestHeaders
      })
        .then(response => {
          return response.json();
        })
        .then(results => {
          let curScope = this;
          let containerObs = results.detected_objects_by_type.container_small;
          let trashBagObs = results.detected_objects_by_type.garbage_bag;
          let cardBoardObs = results.detected_objects_by_type.cardboard;

          containerObs == undefined
            ? (curScope.binCount = 0)
            : (curScope.binCount = containerObs.length);
          trashBagObs == undefined
            ? (curScope.trashCount = 0)
            : (curScope.trashCount = trashBagObs.length);
          cardBoardObs == undefined
            ? (curScope.cardboardCount = 0)
            : (curScope.cardboardCount = cardBoardObs.length);
          curScope.totalCount = curScope.cardboardCount + curScope.trashCount + curScope.binCount
        })

        .catch(er => {
          console.log(er);
        });
    },

    fetchAnalysedFrames() {
      let frameEndpoint = process.env.VUE_APP_API_ENDPOINT.replace(
        "{{APP_ID}}",
        this.appId
      );

      fetch(frameEndpoint, {
        method: "GET",
        headers: this.requestHeaders
      })
        .then(response => {
          return response.json();
        })
        .then(results => {
          // console.log(results)
          let imageUrl = results.take_frame.img;
          this.analysedFrame = imageUrl;
          eventBus.$emit("frameReceived", this.analysedFrame);

          let c = document.getElementById("stream-canvas");
          let ctx = c.getContext("2d");

          ctx.clearRect(0, 0, c.width, c.height);

          // loop for all boxes
          var i;
          for (i = 0; i < results.detected_objects.length; i++) {
            let cord1 = results.detected_objects[i].bbox.coordinate1;
            let cord2 = results.detected_objects[i].bbox.coordinate2;
            let frameMeta = results.frame_meta;
            this.drawBox(cord1, cord2, frameMeta);
          }
        })
        .catch(er => {
          console.log(er);
        });
    },

    todayDateFunc: function(date) {
      let year = date.getFullYear();
      let month = this.addZero(date.getMonth()) + 1;
      let day = this.addZero(date.getDate());

      this.todayDate = year + "-" + month + "-" + day;

      return this.todayDate;
    },

    addZero: function(i) {
      if (i < 10) {
        i = "0" + i;
      }
      return i;
    },

    drawBox: function(cord1, cord2, frameMeta) {
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

      var x1_canvas = x1/width*canvas_width;
      var y1_canvas = y1/height*canvas_height;

      var box_width = (x2 - x1)/width*canvas_width;
      var box_height = (y2 - y1)/height*canvas_height;

      ctx.beginPath();
      ctx.rect(x1_canvas, y1_canvas, box_width, box_height);

      ctx.strokeStyle = "blue";
      ctx.stroke();
    }
  },

  mounted() {
    this.appId = localStorage.appId;
    this.fetchAnalysedResults();
    setInterval(this.fetchAnalysedFrames, 5000);
    // FETCH ANALYSED DATA EVERY 9 SECOND
    setInterval(this.fetchAnalysedResults, 5000);
  }
};
</script>
<style>
.count-box-one {
  display: flex;
  justify-content: space-around;
  margin-right: 2rem;
}

.count-box-two {
  align-self: center;
}

.stream-counts {
  transform: rotate(90deg);
  color: white;
}

#stream-frame {
  /* width: 50% !important;
  height: 75% !important; */
  height: 125px;
  width: 125px;
  background: grey;
  transform: rotate(90deg);
  position: absolute;
  /* right: 20px; */
  /* top: 0; */
  /* right: 0; */
  z-index: 1;
  /* border: 2px solid green; */
}

#stream-canvas {
  /* background: red; */
  transform: rotate(90deg);
  /* border: 2px solid red; */
  height: 125px;
  width: 125px;
  position: absolute;
  /* right: 20px; */
  /* top: 0; */
  /* right: 0; */
  z-index: 2;
}

.total-counts {
  font-size: 2.5rem;
  color: white;
}

.icons {
  height: 3rem;
  width: 3rem;
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
</style>
