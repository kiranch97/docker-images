<template>
  <div id="container">
    <div id="image-section">
      <img id="intro-img" src="../assets/pwa/intro.png" alt />
    </div>
    <div id="text-section">
      <div id="header-section">
        <p class="odk-title" id="title">Object Detection Kit</p>
        <p class="body-1">Keep streets clean by scanning garbage while driving</p>
      </div>
      <div id="buttons-section">
        <router-link to="/recommendation">
          <b-button @click="saveWorkerId()" rounded id="cto-button" size="is-medium">Ik ben een gemeente chauffer</b-button>
        </router-link>
        <router-link to="/recommendation">
          <b-button @click="saveDemoId()" rounded id="gitlab-button" size="is-medium">Ik ben een demo gebruiker</b-button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "pwa-startpage",
  data() {
    return {};
  },
  methods: {
    checkAppMode() {
      if (window.matchMedia("(display-mode: standalone)").matches) {
        console.log("This is running as standalone.");
      } else {
        console.log("This is running on the browser");
        // this.$router.push({ path: "/" });
      }
    },
    checkExistingId: function() {
      if (localStorage.appId && localStorage.userType) {
        this.$router.push({ path: "/client" });
        this.appId = localStorage.appId;
        this.userType = localStorage.userType;
      } else {
        this.generateId();
      }
    },

    // ----

    generateId: function() {
      let uniqueId = Math.random()
        .toString(32)
        .substring(3);
      localStorage.appId = uniqueId;
    },

    // ----

    saveWorkerId: function() {
      localStorage.userType = "waste_department";
      console.log("submitted!");
    },

    // ----

    saveDemoId() {
      localStorage.userType = "demo";
      console.log("submitted!");
    }
  },
  mounted() {
    this.checkAppMode();
  }
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
  justify-content: center;
  align-items: center;
  height: 50%;
  width: 100%;
  text-align: left;
}

#buttons-section {
  height: 30%;
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
  height: 100%;
}

#intro-img {
  object-fit: cover;
}

@media (max-width: 1024px) and (orientation: portrait) {
  #container {
    background: var(--second-white-color);
    width: 100%;
    height: 100%;
    top: 0;
  }

  #image-section {
    display: flex;
    justify-content: flex-start;
  }
}

@media (max-width: 1024px) and (orientation: landscape) {
  #container {
    top: 0;
    height: 100%;
    max-width: none;
    max-height: none;
  }

}
</style>