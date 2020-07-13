<template>
  <div class="container">
    <div class="image-section">
      <img class="intro-img" src="../assets/pwa/intro.png" alt>
    </div>

    <div class="text-section">
      <div class="header-section">
        <h1>Object Detection Kit</h1>
        <p>Houd de straten schoon door te scannen tijdens het rijden</p>
      </div>

      <div class="buttons-section">
        <router-link
          to="/recommendation"
          tag="b-button"
          class="is-secondary is-rounded is-expanded"
        >
          Beginnen
        </router-link>
      </div>
    </div>
  </div>
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

<style scoped>
.container {
  position: relative;
  width: 100vw;
  height: 100vh;
  max-width: 896px;
  max-height: 414px;
  margin: 0 auto;
  padding: 0 2rem 0 1rem;
  background: var(--color-white-bis);
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.image-section {
  width: 50%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.intro-img {
  object-fit: cover;
  transform: translateX(-15%);
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
  margin-top: 2rem;
}

.buttons-section {
  width: 100%;
  display: flex;
  flex-direction: column;
}
</style>
