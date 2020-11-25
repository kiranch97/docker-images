<template>
  <odk-container>
    <div class="image-section">
      <img src="@/assets/pwa/intro.png" alt>
    </div>

    <div class="text-section">
      <div class="text-section-header">
        <h1 class="odk-title">Object Detection Kit</h1>
        <p class="caption-1">Houd de straten schoon door te scannen tijdens het rijden</p>
      </div>

      <div class="text-section-buttons">
        <!-- Login -->
        <router-link
          to="/user"
          tag="b-button"
          class="is-secondary is-rounded is-expanded"
        >
          Inloggen
        </router-link>

        <!-- Start trial / Demo user -->
        <b-button
          class="is-primary is-outlined is-rounded is-expanded"
          @click="saveDemo()"
        >
          Nu uitproberen
        </b-button>
      </div>
    </div>
  </odk-container>
</template>

<script>
import { startupCheck } from "@/mixins/startupCheck";

export default {
  name: "WelcomePage",

  mixins: [ startupCheck ],

  data () {
    return {};
  },

  mounted () {
    // Check if the user is already logged in,
    // if so, go to streaming client
    this.checkUserType();
  },

  methods: {
    saveDemo () {
      this.$router.push("/trial");
    },

    // --

    sendToClient () {
      this.$router.push("/client");
    },

    // --

    checkUserType () {
      // If user has type
      if (localStorage.userType) {
        // send to client
        this.sendToClient();
      } 
      // If user has no type
      else {
        // clear remaining localStorage
        localStorage.clear();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.image-section {
  display: flex;
  align-items: center;
  justify-content: center;

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
  }

  &-buttons {
    display: flex;
    flex-direction: column;
    width: 100%;

    .button {
      width: 100%;

      &:nth-child(1) {
        margin-bottom: 1rem;
      }
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
