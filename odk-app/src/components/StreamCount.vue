<template>
  <div id="stream-results">
    <div
      id="stream-total"
      :class="{ bounce }"
    >
      <p class="total-counts">{{ totalCount }}</p>
    </div>

    <swiper
      v-show="false"
      id="swiper"
      :options="swiperOption"
      style="overflow: visible;"
    >
      <swiper-slide
        v-for="item in orderSwiperItems"
        :key="item.id"
        class="swiper-item"
      >
        <img class="icons" :src="require(`../assets/objects/${item.itemPicture}.png`)">

        <p v-if="item.count > 0" class="count">{{ item.count }}</p>

        <div :class="{ 'count-fade': item.count }" />
      </swiper-slide>
    </swiper>
  </div>
</template>

<script>
export default {
  name: "StreamCount",

  props: {
    websocketStreamState: {
      type: String,
      default: "off",
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
      bounce: false,
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

      return this._.orderBy(swiperItems, "count", "desc");
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

    totalCount (newCount, oldCount) {
      if (newCount > oldCount) {
        clearTimeout(this.bounceAnimEnd);
        this.bounce = true;

        this.bounceAnimEnd = setTimeout(() => {
          this.bounce = false;
        }, 250);
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

          this.binCount = results.container_small || 0;
          this.trashCount = results.garbage_bag || 0;
          this.cardboardCount = results.cardboard || 0;
          this.matrasCount = results.matras || 0;
          // this.christmasTreeCount = results.christmas_tree || 0;
          // this.constructionBinCount = results.construction_container || 0;

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

<style lang="scss">
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

#stream-total {
  width: 4.5rem;
  height: 5.5rem;
  background: var(--color-purple);
  border-bottom-right-radius: 2.25rem;
  border-bottom-left-radius: 2.25rem;
  z-index: 2;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 250ms ease-in-out;

  &.bounce {
    transform: scale(1.2);
  }
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
