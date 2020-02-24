<template>
  <div id="stream-results">
    <div id="stream-total">
      <p class="total-counts">{{ totalCount }}</p>
    </div>
    <swiper id="swiper" :options="swiperOption">
      <swiper-slide class="swiper-item">
        <img class="icons" src="../assets/objects/Cardboard.png" />
        <p v-if="cardboardCount > 0" class="count">{{ cardboardCount }}</p>
        <div :class="{ 'count-fade': cardboardCount }"></div>
      </swiper-slide>
      <swiper-slide class="swiper-item">
        <img class="icons" src="../assets/objects/garbage-bag.png" />
        <p v-if="trashCount > 0" class="count">{{ trashCount }}</p>
        <div :class="{ 'count-fade': trashCount }"></div>
      </swiper-slide>
      <swiper-slide class="swiper-item">
        <img class="icons" src="../assets/objects/Garbage-bins.png" />
        <p v-if="binCount > 0" class="count">{{ binCount }}</p>
        <div :class="{ 'count-fade': binCount }"></div>
      </swiper-slide>
      <swiper-slide class="swiper-item">
        <img class="icons" src="../assets/objects/Christmas-tree.png" />
      </swiper-slide>
      <swiper-slide class="swiper-item">
        <img class="icons" src="../assets/objects/Construction-container.png" />
      </swiper-slide>
      <swiper-slide class="swiper-item">
        <img class="icons" src="../assets/objects/Matresses.png" />
      </swiper-slide>
      <div class="swiper-pagination" slot="pagination"></div>
    </swiper>
  </div>
</template>
<script>
// import { eventBus } from "../main";

export default {
  name: "stream-count",

  props: ["websocketStreamState"],

  watch: {
    websocketStreamState() {
      if (this.websocketStreamState == null || this.websocketStreamState === "off") {
        this.fetchAnalysedResults();
        console.log("Fetch only once");
      } else if (this.websocketStreamState == "on") {
        setInterval(this.fetchAnalysedResults, this.countFetchRate);
        console.log("Keep fetching");
      }
    }
  },

  data() {
    return {
      swiperOption: {
        direction: "vertical",
        pagination: {
          clickable: true
        },
        slidesPerView: 5,
        spaceBetween: 15,
        freeMode: true
      },
      /// -------
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
      console.log("Websocket Stream State:" + this.websocketStreamState);

      let curEndPointBase =
        this.apiHttpUrl + "/detected_objects?app_id={{APP_ID}}&day={{DATE}}";

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
          if (results.length == 0) return;

          let curScope = this;

          curScope.binCount =
            results.detected_objects_by_type.container_small || 0;
          curScope.trashCount =
            results.detected_objects_by_type.garbage_bag || 0;
          curScope.cardboardCount =
            results.detected_objects_by_type.cardboard || 0;

          curScope.totalCount =
            curScope.binCount + curScope.trashCount + curScope.cardboardCount;
        })
        .catch(er => {
          console.log("==> Error occured in 'fetchAnalysedResults':" + er);
        });
    },

    todayDateFunc(date) {
      let year = date.getFullYear();
      let month = this.addZero(date.getMonth() + 1);
      let day = this.addZero(date.getDate());
      this.todayDate = year + "-" + month + "-" + day;

      return this.todayDate;
    },

    addZero(i) {
      if (i < 10) {
        i = "0" + i;
      }
      return i;
    }
  },

  mounted() {
    this.appId = localStorage.appId;
    this.userType = localStorage.userType;

    console.log(
      "=> Starting 'fetchAnalysedResults' with 'countFetchRate': " +
        this.countFetchRate
    );
    // setInterval(this.fetchAnalysedResults, this.countFetchRate);
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

#stream-results {
  width: 15%;
  height: 426px;
  /* border: 2px solid yellow; */
  display: flex;
  flex-direction: column;
  justify-content: flex-start !important;
  /* align-items: center; */
}

#stream-total {
  width: 50px;
  height: 15%;
  display: flex;
  justify-content: center;
  align-items: center;
  /* border: 2px solid black; */
  background: var(--main-purple-color);
  border-bottom-right-radius: 45%;
  border-bottom-left-radius: 45%;
}

.total-counts {
  font-size: 2rem;
  color: white;
}

.icons {
  height: 2rem;
  width: 2rem;
  /* opacity: 0.3; */
}

.count {
  position: absolute;
  left: 0;
  right: 0;
  font-weight: 700;
  font-size: 1.5rem;
  color: white;
  z-index: 5;
}

.count-fade {
  width: 100%;
  height: 100%;
  background: rgba(58, 34, 93, 0.5);
  /* background: rgba(0, 0, 0, 0.16); */
  border-radius: 50%;
  position: absolute;
}

#swiper {
  /* border: 2px solid green; */
  height: 80%;
  padding-top: 1rem;
}

/deep/ .swiper-wrapper {
  justify-content: space-between;
}

.swiper-item {
  width: 50px !important;
  height: 50px !important;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  background: white;
}

@media (max-width: 1024px) and (orientation: landscape) {
  #stream-results {
    height: 20%;
    width: 100%;
  }
}

@media (max-width: 1024px) and (orientation: portrait) {
  #stream-results {
    height: 20%;
    width: 100%;
  }
}
</style>
