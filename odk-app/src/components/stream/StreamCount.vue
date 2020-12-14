<template>
  <div id="stream-counter">
    <div
      id="stream-total"
      :class="{ bounce }"
    >
      <p class="total-counts">{{ totalCount }}</p>
    </div>

    <swiper
      id="swiper"
      :options="swiperOption"
    >
      <swiper-slide
        v-for="obj in orderSwiperItems"
        :key="obj.name"
        class="swiper-item"
      >
        <img class="icons" :src="require(`@/assets/objects/${obj.name}.svg`)">
        <p class="count">{{ obj.count }}</p>
        <div :class="{ 'count-fade': obj.count }" />
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
      objects: [],
      totalCount: 0,
    };
  },

  computed: {
    orderSwiperItems: function () {      
      const items = [];

      // Only use objects where count > 1
      this.objects.forEach(object => {
        if (object.count > 0) {
          items.push(object);
        }
      });

      const orderedItems = this._.orderBy(items, "count", "desc");
      return orderedItems;
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
      const data = await fetchEndpoint(
        "/detected_objects",
        "GET",
        true,
        `?stream_id=${this.streamId}&day=${this.$moment().format("YYYY-MM-DD")}`
      );

      // Check for potential fetch error
      if (data.status && data.status == "error") {
        return;
      }

      // Check if data is empty
      if (this._.isEmpty(data)) {
        console.debug("Fetched with 0 counts");
        return;
      }

      // Remove privacy filter counts
      delete data.face_privacy_filter;
      delete data.license_plate_privacy_filter;

      // Set data
      const objects = [];
      let totalObjects = 0;

      for (const [key, value] of Object.entries(data)) {
        totalObjects += value;
        objects.push(
          {
            name: key,
            count: value,
          }
        );
      }

      // Sort objects
      this.objects = objects;

      // Set total
      this.totalCount = totalObjects;
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
    top: 5rem;
    z-index: 1;
    overflow: visible;

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
        margin: 0;
        color: var(--color-white);
        font-weight: 700;
        font-size: 1.5rem;
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
