<template>
  <odk-container>
    <div class="image-section">
      <img src="../assets/pwa/intro.png" alt>
    </div>

    <div class="text-section">
      <div class="text-section-header">
        <h1>Object Detection Kit</h1>
        <p>Houd de straten schoon door te scannen tijdens het rijden</p>
      </div>

      <div class="text-section-buttons">
        <router-link
          to="/recommendation"
          tag="b-button"
          class="is-secondary is-rounded is-expanded"
        >
          Beginnen
        </router-link>
      </div>
    </div>
  </odk-container>
</template>

<script>
import { startupCheck } from "../mixins/startupCheck";

export default {
  name: "WelcomePage",

  mixins: [ startupCheck ],

  data () {
    return {
      buttonDisabled: true,
    };
  },

  mounted () {
    // Init
    //IF USER IN BROWSER AND development mode is off redirect them to BrowserStartPage
    this.checkAppMode();
    //IF USER HAS LOGGED IN BEFORE use that info but GENERATE NEW streamId for new session
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
  },
};
</script>

<style lang="scss" scoped>
.image-section {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50%;

  img {
    object-fit: cover;
    transform: translateX(-15%);
  }
}

.text-section {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-self: center;
  padding: 2.5rem 0 2.5rem 3rem;
  max-width: 20rem;
  height: 50%;

  &-header {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    margin-top: 2rem;
    width: 100%;
    text-align: left;
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
