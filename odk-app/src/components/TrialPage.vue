<template>
  <odk-container>
    <div class="image-section">
      <img src="../assets/pwa/trial.png" alt>
    </div>

    <div class="text-section">
      <div class="text-section-header">
        <h1 class="odk-title is-4 page-title">
          <router-link to="/welcome">
            <img
              svg-inline
              svg-sprite
              src="@/assets/ui/chevron-left.svg"
              alt="Ga terug"
              class="back-button"
            >
          </router-link>
          ODK uitproberen
        </h1>
        <p class="caption-1">
          Tijdens het uitproberen van de App worden uw scan resultaten niet opgeslagen. 
          Als u een chauffeur van de gemeente bent, ga dan terug en log in met uw code.
        </p>
      </div>

      <div class="text-section-buttons">
        <!-- Login -->
        <b-button
          class="is-secondary is-rounded is-expanded"
          @click="toRecommendation()"
        >
          Nu uitproberen
        </b-button>
      </div>
    </div>
  </odk-container>
</template>

<script>
export default {
  name: "TrialPage",

  data () {
    return {};
  },

  methods: {
    toRecommendation () {
      localStorage.userType = "demo";
      this.$router.push("/recommendation");
    },
  },
};
</script>

<style lang="scss" scoped>
a::after {
  display: none;
}

.image-section {
  display: flex;
  align-items: flex-start;

  img {
    max-width: 105%;
    object-fit: cover;
    transform: translateX(-15%);
  }
}

.text-section {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-self: center;
  padding: 2.5rem;
  height: 50%;

  &-header {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    margin-top: 1rem;
    width: 100%;
    text-align: left;

    .page-title {
      line-height: 1.2rem;
      display: flex;

      .back-button {
        margin-right: 0.8rem;
        width: 1.25rem;
        height: 1.25rem;
        outline: none;
      }
    }
  }

  &-buttons {
    display: flex;
    flex-direction: column;
    width: 100%;

    .button {
      width: 100%;
    }
  }
}

@media (orientation: landscape) {
  .image-section {
    width: 45%;
    height: auto;
  }

  .text-section {
    width: 55%;
    height: 100%;
    max-height: 414px;
  }
}
</style>
