<template>
  <div id="container">
    <div id="image-section">
      <img id="intro-img" src="../assets/pwa/intro.png" alt />
    </div>
    <div id="text-section">
      <div id="header-section">
        <p class="odk-title" id="title">Object Detection Kit</p>
        <p class="body-1">Houd de straten schoon door te scannen tijdens het rijden</p>
      </div>
      <div id="buttons-section">
        <router-link to="/login">
          <button @click="saveWorkerId()" id="yellow-button" size="is-medium">Gemeente chauffer</button>
        </router-link>
        <router-link to="/client">
          <button @click="saveDemoId()" id="transparent-button" size="is-medium">Demo gebruiker</button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "user-page",
  data() {
    return {
      buttonDisabled: true
    };
  },

  // ----

  methods: {
    checkAppMode() {
      let checkMedia = window.matchMedia("(display-mode: standalone)").matches;
      if (checkMedia) {
        console.log("This is running as standalone.");
      } else {
        console.log("This is running on the browser");
        // process.env.VUE_APP_APP_MODE
        //   ? console.log("development mode")
        //   : this.$router.push({ path: "/" });
      }
    },

    // ----

    checkIDUsertype() {
      if (localStorage.appId && localStorage.userType) {
        this.$router.push("/client");
      } else {
        this.generateId();
        console.log("ID Generated");
      }
    },

    // ----

    generateId() {
      let uniqueId = Math.random()
        .toString(32)
        .substring(3);
      localStorage.appId = uniqueId;
    },

    // ----

    saveWorkerId() {
      localStorage.userType = "waste_department";
      console.log("Worker id generated!");
    },

    // ----

    saveDemoId() {
      localStorage.userType = "demo";
      console.log("Demo id generated");
    }
  },

  // ----
  
  mounted() {
    // Init
    //IF USER IN BROWSER AND development mode is off redirect them to BrowserStartPage
    this.checkAppMode();
    //IF USER DOESNT HAVE ID YET GENERATE ON FOR THEM
    this.checkIDUsertype();
  }
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

#intro-img {
  object-fit: cover;
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
  margin-top: 2rem;
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

@media screen and (max-width: 660px) {
}
</style>