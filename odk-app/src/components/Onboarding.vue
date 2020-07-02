<template>
  <div id="container">
    <swiper :options="swiperOption" class="swiper-box">
      <swiper-slide class="swiper-item">
        <div class="item-1">
          <img id="logo" src="../assets/odk-logo.png" />
          <router-link to="login" tag="li">
            <b-button class="skip-button" type="is-text">Skip</b-button>
          </router-link>
        </div>
        <div class="item-2">
          <div class="info-box">
            <h1 class="onboarding-header">Scan to keep streets clean</h1>
            <p class="onboarding-info">
              ODK app allows you to scan garbage on the streets and
              automatically report to the responsible services
            </p>
          </div>
          <b-button
            @click="toggleBullets = !toggleBullets"
            class="swiper-next"
            type="is-text"
            >Show me how it works</b-button
          >
        </div>
      </swiper-slide>
      <swiper-slide class="swiper-item">
        <div class="item-1">
          <img class="onboarding-image" src="../assets/rotate.png" />
          <router-link to="login" tag="li">
            <b-button class="skip-button-2" type="is-text">Skip</b-button>
          </router-link>
        </div>
        <div class="item-2">
          <div id="info-box-one">
            <h1 class="onboarding-header">Switch to landscape mode</h1>
            <p class="onboarding-info">
              With landscape mode you can get a wider angle for the stream
            </p>
          </div>
        </div>
      </swiper-slide>
      <swiper-slide class="swiper-item">
        <div class="item-1">
          <img class="onboarding-image" src="../assets/battery.png" />
          <router-link to="login" tag="li">
            <b-button class="skip-button-2" type="is-text">Skip</b-button>
          </router-link>
        </div>
        <div class="item-2">
          <div class="info-box-two">
            <h1 class="onboarding-header">Keep Battery in charge</h1>
            <p class="onboarding-info">
              If you are going to use the stream for a while
            </p>
          </div>
        </div>
      </swiper-slide>
      <swiper-slide class="swiper-item">
        <div class="item-1">
          <img class="onboarding-image" src="../assets/data.png" />
          <router-link to="login" tag="div">
            <b-button class="skip-button" type="is-text">Skip</b-button>
          </router-link>
        </div>
        <div class="item-2">
          <div class="info-box-three">
            <h1 class="onboarding-header">Check data usage</h1>
            <p class="onboarding-info">
              An unlimited data subscription is recommended
            </p>
          </div>
        </div>
      </swiper-slide>
      <swiper-slide class="swiper-item">
        <div class="item-1">
          <img class="onboarding-image" src="../assets/toggle.png" />
          <router-link to="login" tag="div">
            <b-button class="skip-button" type="is-text">Next</b-button>
          </router-link>
        </div>
        <div class="item-2">
          <div class="info-box-four">
            <h1 class="onboarding-header">Toggle Streaming mode</h1>
            <p class="onboarding-info">
              Auto mode will start and pause based on your vehicle speed. Manual
              mode allows you to control the stream
            </p>
          </div>
        </div>
      </swiper-slide>
      <div
        v-show="toggleBullets"
        class="swiper-pagination"
        slot="pagination"
      ></div>
    </swiper>
  </div>
</template>

<script>
export default {
  name: "onboarding",
  data() {
    return {
      toggleBullets: false,

      //////// SWIPER OPTION \\\\\\\

      swiperOption: {
        direction: "horizontal",
        slidesPerView: 1,
        mousewheel: true,
        pagination: {
          el: ".swiper-pagination",
          clickable: true
        },
        navigation: {
          nextEl: ".swiper-next"
        }
      }
    };
  },

  created(){
    if (localStorage.streamId){
      this.$router.push("/client");
      console.log("Skip onboarding!")
    }
  }
};
</script>

<style scoped>

html,
body {
  position: relative;
  height: 100%;
}
body {
  background: #eee;
}

#container {
  width: 100vw;
  height: 100vh;
}

.swiper-box {
  width: 100%;
  height: 100% !important;
}
.swiper-item {
  display: grid;
  grid-template-rows: 55% 45%;
  height: 100% !important;
  text-align: center;
  background: #fff;
  justify-content: center;
  align-content: center;
}

.item-1 {
  display: flex;
  justify-content: center;
  align-items: center;
}

.item-2 {
  justify-self: center;
  align-self: center;
  height: 100%;
}

#logo {
  height: 0.876rem;
  max-height: 24px;
  width: 3.48rem;
  transform: rotate(-0deg);
}

.onboarding-info {
  text-align: center;
  font-size: 16px;
}

.onboarding-header {
  font-size: 20px;
  font-weight: bold;
}

.onboarding-image {
}

.info-box {
  width: 25rem;
  align-self: end;
}

#info-box-one {
  width: 18rem;
}

.info-box-two {
  width: 16rem;
}

.info-box-three{
  width: 17rem;
}

.info-box-four{
  width: 26rem;
}

.skip-button {
  position: absolute;
  right: 2rem;
  top: 1rem;
  color: blue !important;
  font-size: 1rem;
  font-weight: 500;
  text-decoration: none !important;
}

.skip-button-2 {
  position: absolute;
  right: 2rem;
  top: 1rem;
  color: blue !important;
  font-size: 1rem;
  font-weight: 500;
  text-decoration: none !important;
}

.swiper-next {
  color: blue !important;
  font-weight: 500;
}

</style>
