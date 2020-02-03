<template>
  <div class="login">
    <div class="header">
      <h1 class="login-header">Kies wat voor gebruiker je bent</h1>
    </div>
    <div class="buttons">
      <router-link to="/client" class="login-button" tag="b-button">
        <b-button type="is-info" @click="saveWorkerId()">Afvalafdeling</b-button>
      </router-link>
      <router-link to="/client" class="login-button" tag="b-button">
        <b-button type="is-info" @click="saveDemoId()">Demo</b-button>
      </router-link>
    </div>
  </div>
</template>
<script>
import { required, minLength } from "vuelidate/lib/validators";

export default {
  name: "login",
  data: function() {
    return {
      appId: "",
      userType: ""
    };
  },
  validations: {
    appId: {
      required,
      minLength: minLength(6)
    }
  },
  methods: {
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
    },

    // ----

    handleOnComplete(value) {
      this.appId = value;
      console.log(this.appId);
    }
  },

  mounted() {
    this.checkExistingId();
  }
};
</script>

<style scoped>
.login {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

.login-header {
  font-weight: bold;
  font-size: 1.125rem;
  color: var(--black-color);
  font-family: "Open sans", sans-serif;
  margin-bottom: 2rem;
}

button {
  font-family: "Open sans", sans-serif !important;
  margin: 0!important;
}

.login-button {
  background: transparent !important;
}
</style>
