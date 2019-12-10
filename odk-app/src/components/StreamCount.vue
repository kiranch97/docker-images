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
      binCount: 0,
      trashCount: 0,
      cardboardCount: 0,
      totalCount: 0,
      appId: null,
      requestHeaders: {
        "Content-Type": "application/json",
        Authorization: "No Auth"
      },
      apiHttpUrl: process.env.VUE_APP_API_HTTP_URL,
      countFetchRate: 1000
    };
  },

  methods: {
    fetchAnalysedResults() {
      let curEndPointBase = this.apiHttpUrl + '/detected_objects?app_id={{APP_ID}}&day={{DATE}}'

      let curEndPoint = curEndPointBase
        .replace("{{APP_ID}}", this.appId)
        .replace("{{DATE}}", this.todayDateFunc(new Date()));

      fetch(curEndPoint, {
        method: "GET",
        headers: this.requestHeaders
      })
        .then(response => {
          return response.json();
        })
        .then(results => {
          if (results.length == 0) return

          let curScope = this;

          curScope.binCount = results.detected_objects_by_type.container_small || 0;
          curScope.trashCount = results.detected_objects_by_type.garbage_bag || 0;
          curScope.cardboardCount = results.detected_objects_by_type.cardboard || 0;

          curScope.totalCount  = curScope.binCount + curScope.trashCount + curScope.cardboardCount;
        })
        .catch(er => {
          console.log("==> Error occured in 'fetchAnalysedResults':" + er);
        });
    },

    todayDateFunc(date) {
      let year = date.getFullYear();
      let month = this.addZero(date.getMonth()) + 1;
      let day = this.addZero(date.getDate());
      this.todayDate = year + "-" + month + "-" + day;

      return this.todayDate;
    },

    addZero(i) {
      if (i < 10) {
        i = "0" + i;
      }
      return i;
    },
  },

  mounted() {
    this.appId = localStorage.appId;

    console.log("=> Starting 'fetchAnalysedResults' with 'countFetchRate': " + this.countFetchRate)
    setInterval(this.fetchAnalysedResults, this.countFetchRate);
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
