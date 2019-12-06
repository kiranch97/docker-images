<template>
  <div>
    <div class="input-box">
      <div class="box-top"></div>
      <div class="box-mid">
        <div class="box-mid-1">
          <h1 class="onboarding-header">Introduce your license plate</h1>
          <vie-otp-input
            style="justify-content: center;"
            inputClasses="otp-input"
            :numInputs="6"
            separator=""
            :shouldAutoFocus="true"
            @on-complete="handleOnComplete"
          />
          <!-- </b-field> -->
          <!-- <p
            class="error-msg"
            message="this field is required"
            v-if="!$v.appId.required"
          >
            this field is required
          </p> -->
        </div>

        <div class="buttons-box">
          <router-link
            to="/client"
            class="login-button"
            tag="b-button"
            @click.prevent="saveWorkerId()"
          >
            <b-button :disabled="$v.appId.$invalid" type="is-info">Next</b-button>
          </router-link>
          <router-link  to="/client" class="demo-button" tag="li">
            <b-button id="demo" type="is-text">I'm a demo user</b-button>
          </router-link>
        </div>
      </div>
      <div class="box-msg"></div>
    </div>
  </div>
</template>
<script>
import { required, minLength, maxLength } from "vuelidate/lib/validators";

export default {
  name: "login",
  data: function() {
    return {
      appId: ""
    };
  },
  validations: {
    appId: {
      required,
      minLength: minLength(6)
    }
  },
  methods: {
    //On click event Save Localstorage appId into the appId
    //data property and send prop to StreamDetails component
    saveWorkerId: function() {
      localStorage.appId = this.appId;
      // eventBus.$emit("idIsSaved", this.appId);
      console.log("submitted!");
    },

    // ----

    checkExistingId: function() {
      if (localStorage.appId) {
        router.push({ path: "/login" });
        this.appId = localStorage.appId;
      }
    },

    createDemoUserId(){
      let r = Math.random().toString(36).substring(4);
      let uniqueId = "user" + r ;
      localStorage.appId = uniqueId;
      // eventBus.$emit("idIsSaved", uniqueId);
      console.log("submitted!");
    },

    // ----

    handleOnComplete(value) {
      this.appId = value;
      console.log(this.appId);
    }
  },

  watch: {
    appId: function(newappId) {
      localStorage.appId = newappId;
    }
  },

  mounted() {
    this.createDemoUserId()
  }
};
</script>

<style>

:root {
  font-size: 16px;
}

 *{
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}


element {
  --main-purple-color: #3a225d;
  --red-color: #e1524a;
  --pink-color: #c83760;
  --yellow-color: #f6d365;
}

.otp-input {
  width: 30px !important;
  height: 40px !important;
  padding: 5px;
  margin: 5px;
  font-size: 20px;
  border-radius: 4px;
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.5);
  text-align: center;
  color: rgba(0, 0, 0, 0.5);
}

.otp-input.error {
  border: 1px solid red !important;
}

p,
input,
button {
  font-family: "Open sans", sans-serif !Important;
  font-style: normal;
}

::placeholder {
  opacity: 50%;
}

.input-box {
  height: 100vh;
  width: 100vw;
  background: #fff;
  transition: 0.2s;
  display: grid;
  grid-template-columns: 20% 60% 20%;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
}

.error-msg {
  font-size: 14px;
  margin-top: 20px;
  color: red;
}

.box-top {
  display: flex;
  justify-content: center;
  align-items: flex-end;
}

.box-mid {
  height: 100%;
  align-self: center;
  display: grid;
  grid-auto-rows: 70% 1fr;
}

.box-mid-1 {
  align-self: end;
  margin-bottom: 45px;
}

.box-msg {
  display: flex;
  justify-content: center;
}

.onboarding-header {
  font-weight: bold;
  font-size: 18px;
  color: black;
  font-family: "Open sans", sans-serif;
  margin-bottom: 1rem;
}

.demo-button {
  margin-top: 25px;
  font-size: 1rem !important;
  list-style-type: none;
}

#demo {
  color: blue;
  font-weight: 500;
}

.login-button {
  list-style-type: none;
  font-size: 1rem !important;
  border: none !important;
}

.buttons-box {
  justify-self: center;
}
</style>
