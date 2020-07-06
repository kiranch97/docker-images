<template>
  <div id="container">
    <div id="image-section">
      <div id="image-section-one">
        <img
          id="recommendation-img"
          :class="{ fade: rmdOne}"
          src="../assets/pwa/recommendation1.png"
          alt
        >
        <img
          id="recommendation-img"
          :class="{ fade: rmdThree}"
          src="../assets/pwa/recommendation3.png"
          alt
        >
      </div>
      <div id="image-section-two">
        <img
          id="recommendation-img"
          :class="{ fade: rmdTwo}"
          src="../assets/pwa/recommendation2.png"
          alt
        >
      </div>
    </div>
    <div id="text-section">
      <div id="header-section">
        <p class="caption-1">Het wordt aanbevolen om</p>
        <p id="title" class="odk-title">Uw telefoon op te laden</p>
        <p id="body" class="body-1">tijdens het rijden. Het streamen verbruikt veel batterij</p>
      </div>
      <div id="buttons-section">
        <button
          id="yellow-button"
          rounded
          size="is-medium"
          @click="switchRmd()"
        >
          Volgende
        </button>
        <router-link to="/checklist">
          <button id="transparent-button" rounded size="is-medium">Overslaan</button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RecommendationPage",

  data () {
    return {
      rmdOne: true,
      rmdTwo: false,
      rmdThree: false,
    };
  },
  mounted () {
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

    // ----

    generateId () {
      const uniqueId = Math.random()
        .toString(32)
        .substring(3);
      return uniqueId;
    },

    // ----

    switchRmd () {
      //SWITCH THROUGH THE OPTIONS AND REDIRECT THE USERS TO THE CHECKLIST PAGE
      if (this.rmdOne) {
        this.rmdOne = !this.rmdOne;
        this.rmdTwo = !this.rmdTwo;
        document.getElementById("title").innerHTML =
          "Uw dataverbruik te controleren";
        document.getElementById("body").innerHTML =
          "Het streamen kost veel data. Een ongelimiteerd abonnement wordt geadviseerd";
      } else if (this.rmdTwo) {
        this.rmdTwo = !this.rmdTwo;
        this.rmdThree = !this.rmdThree;
        document.getElementById("transparent-button").style.display = "none";
        document.getElementById("title").innerHTML = "Uw eigen modus te kiezen";
        document.getElementById("body").innerHTML =
          "Met handmatige modus kunt u er zelf voor kiezen wanneer u wilt streamen. De automatische modus zal de stream kunnen starten en stoppen op basis van uw rijsnelheid";
        document.getElementById("buttons-section").style.justifyContent =
          "flex-end";
      } else if (this.rmdThree) {
        this.$router.push("/checklist");
      }
    },

    skipRmd () {
      this.$router.push("/checklist");
    },
  },
};
</script>

<style scoped>
#container {
  position: relative;
  width: 100vw;
  height: 100vh;
  max-width: 896px;
  max-height: 414px;
  margin: 0 auto;
  padding: 0 2rem 0 1rem;
  background: var(--second-white-color);
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

#image-section {
  width: 50%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

#image-section-one {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

#image-section-two {
  display: flex;
}

.odk-title {
  line-height: 1.75rem !important;
}

.rmdimageone {
  max-height: 150px;
  object-fit: contain;
  margin: 1rem;
}

#recommendation-img {
  max-height: 150px;
  object-fit: contain;
  opacity: 0.5;
  margin: 1rem;
}

.fade {
  opacity: 1 !important;
}

#text-section {
  width: 50%;
  height: 100%;
  max-width: 20rem;
  padding: 2.5rem 0 2.5rem 3rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

#header-section {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  text-align: left;
  width: 100%;
}

#buttons-section {
  width: 100%;
  display: flex;
  flex-direction: column;
}

#yellow-button,
#transparent-button {
  width: 100%;
  font-family: "Open Sans", sans-serif;
  font-size: 1rem;
  font-weight: 600;
  text-align: center;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 30px;
}

#yellow-button {
  background: var(--yellow-color);
  color: var(--second-purple-color);
}

#yellow-button:active {
  background: rgba(246, 211, 101, 0.7);
}

#yellow-button:disabled {
  background: #edebf2;
  color: #b8b1c3;
}

#transparent-button {
  background: transparent;
  color: var(--second-purple-color);
  border: 2px solid var(--second-purple-color);
  margin-top: 1rem;
}

#transparent-button:active {
  background: rgba(105, 89, 133, 0.6);
}

@media screen and (max-width: 756px) {
  .odk-title {
    font-size: 1.25rem !important;
  }

  .body-1 {
    font-size: 0.9rem !important;
    line-height: 1.25rem !important;
  }

  #yellow-button,
  #transparent-button {
    font-size: 0.9rem;
  }
}
</style>
