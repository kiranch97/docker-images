<template>
  <div id="stream-results">
    <div id="stream-total">
      <p class="total-counts">{{ totalCount }}</p>
    </div>

    <swiper id="swiper" :options="swiperOption">
      <swiper-slide v-for="item in orderSwiperItems" :key="item.id" class="swiper-item">
        <img class="icons" :src="require(`../assets/objects/${item.itemPicture}.png`)">

        <p v-if="item.count > 0" class="count">{{ item.count }}</p>

        <div :class="{ 'count-fade': item.count }" />
      </swiper-slide>
    </swiper>
  </div>
</template>

<script>
import _ from "lodash";

export default {
  name: "StreamCount",

  props: {
    websocketStreamState: {
      type: String,
      default: () => {},
    },
  },

  data () {
    return {
      // ---- settings ----
      SETTINGS: {
        REQUEST_COUNTS_EVERY_MS: process.env.VUE_APP_RESULT_INTERVAL,
      },
      // ---- end settings ----
      // ----
      swiperOption: {
        direction: "vertical",
        slidesPerView: 5,
        spaceBetween: 15,
        freeMode: true,
      },
      // ----
      //Detectable objects counts
      binCount: 0,
      trashCount: 0,
      cardboardCount: 0,
      christmasTreeCount: 0,
      constructionBinCount: 0,
      matrasCount: 0,
      totalCount: 0,
      requestHeaders: {
        "Content-Type": "application/json",
        Authorization: "No Auth",
      },
      // eslint-disable-next-line no-undef
      apiHttpUrl: process.env.VUE_APP_API_HTTP_URL,
      countFetchRate: 1000,
      fetchResults: null,
    };
  },

  computed: {
    orderSwiperItems: function () {
      const swiperItems = [
        {
          itemPicture: "Cardboard",
          count: this.cardboardCount,
        },
        {
          itemPicture: "Garbage-bag",
          count: this.trashCount,
        },
        {
          itemPicture: "Garbage-bins",
          count: this.binCount,
        },
        // {
        //   itemPicture: "Christmas-tree",
        //   count: this.christmasTreeCount
        // },
        // {
        //   itemPicture: "Construction-container",
        //   count: this.constructionBinCount,
        // },
        {
          itemPicture: "Matresses",
          count: this.matrasCount,
        },
      ];

      return _.orderBy(swiperItems, "count", "desc");
    },
  },

  watch: {
    // Fetch results (counts) when websocket connection
    websocketStreamState () {
      if (
        this.websocketStreamState == null ||
        this.websocketStreamState === "off"
      ) {
        clearInterval(this.fetchResults);
        this.fetchAnalysedResults();
      } else if (this.websocketStreamState == "on") {
        this.fetchResults = setInterval(
          this.fetchAnalysedResults,
          this.SETTINGS.REQUEST_COUNTS_EVERY_MS
        );
      }
    },
  },

  mounted () {
    // Retrieve streamId and userType
    this.streamId = localStorage.streamId;
    this.userType = localStorage.userType;

    // Fetch once when landing
    this.fetchAnalysedResults();
  },

  methods: {
    fetchAnalysedResults () {
      const curEndPointBase =
        this.apiHttpUrl + "/detected_objects?stream_id={{STREAM_ID}}&day={{DATE}}";

      const curEndPoint = curEndPointBase
        .replace("{{STREAM_ID}}", this.streamId)
        .replace("{{DATE}}", this.todayDateFunc(new Date()));

      fetch(curEndPoint, {
        method: "GET",
        headers: this.requestHeaders,
      })
        .then(response => {
          return response.json();
        })
        .then(results => {
          if (results.length == 0) return;

          this.binCount = results.detected_objects_by_type.container_small || 0;
          this.trashCount = results.detected_objects_by_type.garbage_bag || 0;
          this.cardboardCount = results.detected_objects_by_type.cardboard || 0;
          this.matrasCount = results.detected_objects_by_type.matras || 0;
          // this.christmasTreeCount = results.detected_objects_by_type.christmas_tree || 0;
          // this.constructionBinCount = results.detected_objects_by_type.construction_container || 0;

          this.totalCount =
            this.binCount +
            this.trashCount +
            this.cardboardCount +
            this.matrasCount;
            // this.christmasTreeCount +
            // this.constructionBinCount +
        })
        .catch(er => {
          console.log("==> Error occured in 'fetchAnalysedResults':" + er);
        });
    },

    todayDateFunc (date) {
      const year = date.getFullYear();
      const month = this.addZero(date.getMonth() + 1);
      const day = this.addZero(date.getDate());
      this.todayDate = year + "-" + month + "-" + day;

      return this.todayDate;
    },

    addZero (i) {
      if (i < 10) {
        i = "0" + i;
      }

      return i;
    },
  },
};
</script>

<style>
.count-box-one {
  margin-right: 2rem;
  display: flex;
  justify-content: space-around;
}

.count-box-two {
  align-self: center;
}

.stream-counts {
  color: var(--color-white);
  transform: rotate(90deg);
}

#stream-results {
  width: 50px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-start !important;
}

#stream-total {
  width: 50px;
  height: 50px;
  background: var(--color-purple);
  border-bottom-right-radius: 50%;
  border-bottom-left-radius: 50%;
  z-index: 2;
  display: flex;
  justify-content: center;
  align-items: center;
}

.total-counts {
  font-size: 1.5rem;
  color: var(--color-white);
}

.icons {
  width: 2rem;
  height: 2rem;
}

.count {
  position: absolute;
  left: 0;
  right: 0;
  font-weight: 700;
  font-size: 1.5rem;
  color: var(--color-white);
  z-index: 1;
}

.count-fade {
  position: absolute;
  width: 100%;
  height: 100%;
  background: rgba(58, 34, 93, 0.5);
  border-radius: 50%;
}

#swiper {
  position: absolute;
  height: 100vh;
  top: 4rem;
  z-index: 1;
}

.swiper-item {
  width: 50px !important;
  height: 50px !important;
  border-radius: 50%;
  background: var(--color-white);
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
