<template>
  <div id="container">
    <div id="image-section">
      <div id="image-section-one">
        <img
          v-bind:class="{ fade: rmdOne}"
          id="recommendation-img-1"
          src="../assets/pwa/recommendation1.png"
          alt
        />
        <img
          v-bind:class="{ fade: rmdThree}"
          id="recommendation-img-3"
          src="../assets/pwa/recommendation3.png"
          alt
        />
      </div>
      <div id="image-section-one">
        <img
          v-bind:class="{ fade: rmdTwo}"
          id="recommendation-img-2"
          src="../assets/pwa/recommendation2.png"
          alt
        />
      </div>
    </div>
    <div id="text-section">
      <div id="header-section">
        <p class="body-1">Het wordt aanbevolen om</p>
        <p class="odk-title" id="title">Uw telefoon op te laden</p>
        <p class="body-1" id="body">tijdens het rijden. Het streamen verbruikt veel batterij</p>
      </div>
      <div id="buttons-section">
        <b-button @click="switchRmd()" rounded id="cto-button" size="is-medium">Volgende</b-button>
        <router-link to="/checklist">
          <b-button rounded id="gitlab-button" size="is-medium">Overslaan</b-button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "recommendation-page",
  data() {
    return {
      rmdOne: true,
      rmdTwo: false,
      rmdThree: false
    };
  },
  methods: {
    switchRmd() {
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
        document.getElementById("gitlab-button").style.display = "none";
        document.getElementById("title").innerHTML = "Uw eigen modus te kiezen";
        document.getElementById("body").innerHTML =
          "Met handmatige modus kunt u er zelf voor kiezen wanneer u wilt streamen. De automatische modus zal de stream kunnen starten en stoppen op basis van uw rijsnelheid";
        document.getElementById("buttons-section").style.justifyContent =
          "flex-end";
      } else if (this.rmdThree) {
        this.$router.push({ path: "/checklist" });
      }
    },
    skipRmd() {
      this.$router.push({ path: "/checklist" });
    }
  },
  mounted() {}
};
</script>

<style scoped>
.odk-title {
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 2.125rem;
  color: var(--dark-blue-color);
  margin-bottom: 0.75rem;
  width: 15rem;
}

.body-1 {
  font-family: "Open Sans", sans-serif;
  font-size: 1rem;
  font-weight: 400;
  line-height: 26px;
  color: var(--dark-blue-color);
  width: 15rem;
}

#cto-button {
  background: var(--yellow-color);
  color: var(--second-purple-color);
  font-family: "Open Sans", sans-serif;
  font-size: 1rem;
  font-weight: 600; /*semi- bold */
  line-height: 22px;
  width: 16rem;
  height: 2.625rem;
  position: relative;
  outline: none;
}

#cto-button:hover {
  background: rgba(246, 211, 101, 0.7) !important;
}

#gitlab-button {
  width: 16rem;
  height: 2.625rem;
  color: var(--second-purple-color) !important;
  border: 2px solid var(--second-purple-color) !important;
  font-family: "Open Sans", sans-serif !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  outline: none;
}

#gitlab-button:hover {
  background: rgba(105, 89, 133, 0.6);
}

#container {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 50%;
  justify-content: center;
  align-items: center;
  background: var(--second-white-color);
  max-height: 500px;
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  top: 3rem;
}

#text-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
}

#header-section {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  margin-top: 1rem;
  align-items: center;
  height: 15rem;
  width: 100%;
  text-align: left;
}

#buttons-section {
  height: 10rem;
  margin-bottom: 1rem;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}

#add-to-home {
  font-weight: 700;
}

#image-section {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin-top: 1rem;
  margin-bottom: 1rem;
}

#image-section-one {
  display: flex;
  flex-direction: column;
}

.rmdimageone {
  max-height: 150px;
  object-fit: contain;
  margin: 1rem;
}
#recommendation-img-1 {
  max-height: 150px;
  object-fit: contain;
  opacity: 0.5;
  margin: 1rem;
}

#recommendation-img-2 {
  max-height: 150px;
  object-fit: contain;
  opacity: 0.5;
  margin: 1rem;
}

#recommendation-img-3 {
  max-height: 150px;
  object-fit: contain;
  opacity: 0.5;
  margin: 1rem;
}

.fade {
  opacity: 1 !important;
}

@media (max-width: 1024px) and (orientation: portrait) {
  #container {
    background: var(--second-white-color);
    width: 100%;
    height: 100%;
    top: 0;
    flex-direction: column;
    max-width: none;
    max-height: none;
  }

  #image-section {
    display: flex;
    justify-content: center;
  }

  #header-section {
    height: 30%;
  }

  #buttons-section {
    height: 30%;
  }
}

@media (max-width: 1024px) and (orientation: landscape) {
  #container {
    height: 100%;
    top: 0;
    max-width: none;
    max-height: none;
  }

  #buttons-section {
    height: 30%;
  }
}
</style>