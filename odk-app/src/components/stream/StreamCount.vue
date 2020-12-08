<template>
  <div id="stream-counter">
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
        <img class="icons" :src="require(`@/assets/objects/${item.itemPicture}.png`)">

        <p v-if="item.count > 0" class="count">{{ item.count }}</p>

        <div :class="{ 'count-fade': item.count }" />
      </swiper-slide>
    </swiper>
  </div>
</template>

<script>
import { eventBus } from "@/main";
import { fetchEndpoint } from "../../utils/fetchEndpoint";

export default {
  name: "StreamCount",

  props: {
    wsStreamState: {
      type: Object,
      default () {
        return {
          connecting: false,
          open: false,
          closed: true,
          paused: false,
        };
      },
    },
  },

  data () {
    return {
      // -- 
      // Env properties
      fetchCountIntervalTime: process.env.VUE_APP_RESULT_INTERVAL,

      // -- 
      // UI properties
      swiperOption: {
        direction: "vertical",
        slidesPerView: 5,
        spaceBetween: 15,
        freeMode: true,
      },
      bounce: false,

      // --
      // Functional page properties
      fetchResults: null,
      streamId: null,

      // --
      // Detectable objects count properties
      binCount: 0,
      trashCount: 0,
      cardboardCount: 0,
      christmasTreeCount: 0,
      constructionBinCount: 0,
      matrasCount: 0,
      totalCount: 0,
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
    wsStreamState (obj) {
      // Do nothing while connecting
      if (obj.connecting) {
        return;
      }

      // Clear interval if no connection
      if (!obj.open || obj.closed || obj.paused) {
        clearInterval(this.fetchResults);
        return;
      }

      // Start interval fetch if connection
      this.fetchResults = setInterval(
        this.fetchAnalysedResults,
        this.fetchCountIntervalTime
      );
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
    eventBus.$on("newStreamId", (uuid) => {
      // Set streamId
      this.streamId = uuid;

      // Fetch once when streamId arrived
      this.fetchAnalysedResults();
    });
  },

  methods: {
    async fetchAnalysedResults () {
      // Fetch data
      const data = await fetchEndpoint("/detected_objects", "GET", true, `?stream_id=${this.streamId}&day=${this.$moment().format("YYYY-MM-DD")}`);

      // Check for potential fetch error
      if (data.status && data.status == "error") {
        return;
      }

      // Set data
      if (data.length == 0) return;

      this.binCount = data.container_small || 0;
      this.trashCount = data.garbage_bag || 0;
      this.cardboardCount = data.cardboard || 0;
      this.matrasCount = data.matras || 0;
      // this.christmasTreeCount = data.christmas_tree || 0;
      // this.constructionBinCount = data.construction_container || 0;

      this.totalCount =
        this.binCount +
        this.trashCount +
        this.cardboardCount +
        this.matrasCount;
        // this.christmasTreeCount +
        // this.constructionBinCount +
    },
  },
};
</script>

<style lang="scss">
#stream-counter {
  flex: 0 1 auto;
  width: 20%;
  display: flex;
  flex-direction: column;
  align-items: center;

  #stream-total {
    width: 2.875rem;
    height: 3.9375rem;
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

    .total-counts {
      margin: 0;
      color: var(--color-white);
    }
  }

  #swiper {
    position: absolute;
    height: 100vh;
    top: 4rem;
    z-index: 1;

    .swiper-item {
      width: 2.875rem !important;
      height: 2.875rem !important;
      border-radius: 50%;
      background: var(--color-white);
      display: flex;
      justify-content: center;
      align-items: center;

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
    }
  }
}
</style>
