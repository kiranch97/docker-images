<template>
  <odk-container>
    <div class="image-section">
      <!-- <div class="image-section-left"> -->
      <img
        class="recommendation-img"
        :class="{ 'is-opaque': step === 0 }"
        src="../assets/pwa/recommendation1-2.png"
        alt
      >
      <img
        class="recommendation-img"
        :class="{ 'is-opaque': step === 1 }"
        src="../assets/pwa/recommendation2-2.png"
        alt
      >
      <!-- </div> -->

      <!-- <div class="image-section-right">
        <img
          class="recommendation-img"
          :class="{ 'is-opaque': step === 2 }"
          src="../assets/pwa/recommendation2.png"
          alt
        >
      </div> -->
    </div>

    <div class="text-section">
      <div class="text-section-header">
        <p class="caption-1">
          {{ content.caption }}
        </p>
        <h1 class="odk-title">
          {{ content.steps[step].title }}
        </h1>
        <p class="caption-1">
          {{ content.steps[step].body }}
        </p>
      </div>

      <transition-group
        name="fadeout"
        tag="div"
        class="text-section-buttons"
      >
        <b-button
          ref="buttonNext"
          key="buttonNext"
          type="is-secondary"
          rounded
          class="fadeout-item"
          @click="switchRmd"
        >
          Volgende
        </b-button>

        <router-link
          v-if="step < 1"
          key="buttonSkip"
          to="/checklist"
          tag="b-button"
          class="is-primary is-rounded is-outlined fadeout-item"
        >
          Overslaan
        </router-link>
      </transition-group>
    </div>
  </odk-container>
</template>

<script>
export default {
  name: "RecommendationPage",

  data () {
    return {
      step: 0,
      content: {
        caption: "Het wordt aanbevolen om",
        steps: [
          {
            title: "Uw telefoon op te laden",
            body: "Het streamen verbruikt veel batterij.",
          },
          {
            title: "Uw dataverbruik te controleren",
            body: "Het streamen kost veel data. Een ongelimiteerd abonnement wordt geadviseerd.",
          },
          // {
          //   title: "Uw eigen modus te kiezen",
          //   body: "Met handmatige modus kunt u er zelf voor kiezen wanneer u wilt streamen. De automatische modus zal de stream kunnen starten en stoppen op basis van uw rijsnelheid.",
          // },
        ],
      },
    };
  },

  mounted () {},

  methods: {
    switchRmd () {
      this.step >= 1 ? this.$router.push("/checklist") : this.step++;

      this.$refs.buttonNext.$el.focus();

      setTimeout(() => {
        this.$refs.buttonNext.$el.blur();
      }, 250);
    },
  },
};
</script>

<style lang="scss" scoped>
.image-section {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;

  // &-left {
  //   display: flex;
  //   flex-direction: column;
  //   justify-content: center;
  // }

  // &-right {
  //   display: flex;
  // }

  .recommendation-img {
    position: absolute;
    max-height: 175px;
    object-fit: contain;
    opacity: 0.5;
    margin: 1rem;
    display: flex;

    &.is-opaque {
      opacity: 1;
      transition: opacity 350ms ease;
    }

    &:nth-child(1) {
      top: 1rem;
      align-self: flex-start;
    }

    &:nth-child(2) {
      bottom: 1rem;
      align-self: flex-end;
      transform: translateX(1rem);
    }
  }
}

.text-section {
  display: flex;
  flex-direction: column;
  align-self: center;
  justify-content: space-between;
  padding: 2.5rem;
  height: 50%;

  &-header {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    width: 100%;
    text-align: left;
  }

  &-buttons {
    display: flex;
    position: relative;
    flex-direction: column;
    width: 100%;

    .button {
      &:last-of-type {
        margin-top: 1rem;
      }
    }
  }
}

// Transition classes
.fadeout-item {
  transition: all 500ms ease-out;
}

.fadeout-enter,
.fadeout-leave-to {
  opacity: 0;
}

.fadeout-leave-active {
  position: absolute;
  width: 100%;
}

@media (orientation: landscape) {
  .image-section {
    width: 45%;
    height: auto;
  }

  .text-section {
    padding: 2.5rem;
    width: 55%;
    height: 100%;
    max-height: 414px;
  }
}
</style>
