<template>
  <div class="container">
    <div class="image-section">
      <div class="image-section-one">
        <img
          class="recommendation-img"
          :class="{ 'is-opaque': step === 0 }"
          src="../assets/pwa/recommendation1.png"
          alt
        >
        <img
          class="recommendation-img"
          :class="{ 'is-opaque': step === 1 }"
          src="../assets/pwa/recommendation3.png"
          alt
        >
      </div>

      <div class="image-section-two">
        <img
          class="recommendation-img"
          :class="{ 'is-opaque': step === 2 }"
          src="../assets/pwa/recommendation2.png"
          alt
        >
      </div>
    </div>

    <div class="text-section">
      <div class="header-section">
        <p class="caption-1">
          {{ content.caption }}
        </p>
        <h1 class="title">
          {{ content.steps[step].title }}
        </h1>
        <p class="body">
          {{ content.steps[step].body }}
        </p>
      </div>

      <transition-group
        name="fadeout"
        tag="div"
        class="buttons-section"
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
          v-if="step < 2"
          key="buttonSkip"
          to="/checklist"
          tag="b-button"
          class="is-primary is-rounded is-outlined fadeout-item"
        >
          Overslaan
        </router-link>
      </transition-group>
    </div>
  </div>
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
            body: "tijdens het rijden. Het streamen verbruikt veel batterij",
          },
          {
            title: "Uw dataverbruik te controleren",
            body: "Het streamen kost veel data. Een ongelimiteerd abonnement wordt geadviseerd",
          },
          {
            title: "Uw eigen modus te kiezen",
            body: "Met handmatige modus kunt u er zelf voor kiezen wanneer u wilt streamen. De automatische modus zal de stream kunnen starten en stoppen op basis van uw rijsnelheid",
          },
        ],
      },
    };
  },

  mounted () {
    // Use data of previous login, but generate a new streamId for the session.
    this.checkCredentials();
  },

  methods: {
    checkCredentials () {
      if (localStorage.streamId) {
        localStorage.streamId = this.generateId();
        this.$router.push({
          name: "streaming-client",
          params: { uniqueId: localStorage.streamId },
        });
      }
    },

    generateId () {
      const uniqueId = Math.random()
        .toString(32)
        .substring(3);

      return uniqueId;
    },

    switchRmd () {
      this.step >= 2 ? this.$router.push("/checklist") : this.step++;

      this.$refs.buttonNext.$el.focus();

      setTimeout(() => {
        this.$refs.buttonNext.$el.blur();
      }, 250);
    },

    skipRmd () {
      this.$router.push("/checklist");
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  position: relative;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  background: var(--color-grey-light);
  padding: 0 2rem 0 1rem;
  width: 100vw;
  max-width: 896px;
  height: 100vh;
  max-height: 414px;
}

.image-section {
  width: 50%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;

  &-one {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  &-two {
    display: flex;
  }
}

.rmdimageone {
  max-height: 150px;
  object-fit: contain;
  margin: 1rem;
}

.recommendation-img {
  max-height: 150px;
  object-fit: contain;
  opacity: 0.5;
  margin: 1rem;
}

.is-opaque {
  opacity: 1;
  transition: opacity 350ms ease;
}

.text-section {
  width: 50%;
  height: 100%;
  max-width: 20rem;
  padding: 2.5rem 0 2.5rem 3rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.header-section {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  text-align: left;
  width: 100%;
}

.caption-1 {
  margin-bottom: .5em;
}

.title {
  margin-bottom: 0;
}

.buttons-section {
  display: flex;
  position: relative;
  flex-direction: column;
  width: 100%;
}

.button {
  &:last-of-type {
    margin-top: 1rem;
  }
}

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
</style>
