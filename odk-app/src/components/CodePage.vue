<template>
  <odk-container>
    <div class="image-section">
      <img src="../assets/pwa/intro.png" alt>
    </div>

    <div class="text-section">
      <div class="text-section-header">
        <h1 class="odk-title is-4 page-title">
          <router-link to="/user">
            <img
              svg-inline
              svg-sprite
              src="@/assets/ui/chevron-left.svg"
              alt="Ga terug"
              class="back-button"
            >
          </router-link>
          Welkom {{ username }}
        </h1>

        <p class="caption-1">Voer uw pincode in</p>

        <div class="input-wrapper">
          <div 
            v-for="number in formData"
            :key="number.id"
          >
            <input
              v-if="number.nr"
              v-model="number.nr"
              class="field-filled"
              placeholder="*"
              disabled
            >
            <input
              v-else
              class="field"
              disabled
            >
          </div>
        </div>
      </div>

      <div class="text-section-buttons">
        <b-button
          id="send-button"
          class="is-secondary is-rounded is-expanded"
          disabled
          @click="sendCode()"
        >
          Inloggen
        </b-button>
      </div>
    </div>

    <div class="numpad-section">
      <div
        v-for="number in numpadNumbers"
        :key="number.id"
        class="numpad-button-box"
        @click="addNumber(number.nr)"
      >
        <div class="numpad-key">
          {{ number.nr }}
        </div>
      </div>

      <div v-if="!solidBackspace" class="numpad-backspace" @click="deleteNumber()">
        <img
          svg-inline
          src="@/assets/ui/backspace.svg"
          alt="Backspace"
        >
      </div>

      <div v-else class="numpad-backspace" @click="deleteNumber()">
        <img
          svg-inline
          src="@/assets/ui/backspace-solid.svg"
          alt="Backspace"
        >
      </div>
    </div>
  </odk-container>
</template>

<script>
export default {
  name: "CodePage",

  props: {
    username: {
      type: String,
      default: "chauffeur",
    },
  },

  data () {
    return {
      formData: [
        {
          nr: "",
        },
        {
          nr: "",
        },
        {
          nr: "",
        },
        {
          nr: "",
        },
        {
          nr: "",
        },
      ],
      passwordList: [],
      numpadNumbers: [
        {
          nr: "1",
        },
        {
          nr: "2",
        },
        {
          nr: "3",
        },
        {
          nr: "4",
        },
        {
          nr: "5",
        },
        {
          nr: "6",
        },
        {
          nr: "7",
        },
        {
          nr: "8",
        },
        {
          nr: "9",
        },
        {
          nr: "0",
        },
      ],
      solidBackspace: false,
    };
  },

  watch: {
    passwordList (list) {
      // Login button styling
      const sendButton = document.getElementById("send-button");
      if (list.length > 4) {
        sendButton.removeAttribute("disabled", "");
        sendButton.setAttribute("enabled", "");
      } else {
        sendButton.setAttribute("disabled", "");
        sendButton.removeAttribute("enabled", "");
      }
    },
  },

  mounted () {
    setTimeout(() => {
      this.showNumpad();
    }, 750);
  },

  methods: {
    addNumber (clickedNr) {
      if (this.passwordList.length < 5) {
        this.passwordList.push(clickedNr);
        for (let f = 0; f < this.formData.length; f++) {
          const el = this.formData[f];
          if (el.nr == "") {
            el.nr = clickedNr.toString();
            break;
          }
        }
      }
    },

    // --

    deleteNumber () {
      // Get last added number (array-wise)
      const lastNr = this.passwordList.length - 1;

      // Trigger if code contains at least 1 digit
      if (lastNr > -1) {
        // Backspace button styling > solid
        this.solidBackspace = true;

        // Pop digit from list
        this.passwordList.pop();

        // Delete number from formData
        for (let f = 0; f < this.formData.length; f++) {
          const el = this.formData[f];
          if (f == lastNr) {
            el.nr = "";
            break;
          }
        }

        // Backspace button styling > !solid
        setTimeout(() => {
          this.solidBackspace = false;
        }, 200);
      }
    },

    // --

    sendCode () {
      let code = "";
      this.passwordList.forEach((el) => {
        code += el.toString();
      });
      console.log(code);
      localStorage.userType = "worker";
      localStorage.userId = code;
      localStorage.vehicleType = this.username;
      this.$router.push("/recommendation");
    },

    // --

    showNumpad () {
      const imageSection = document.getElementsByClassName("image-section")[0];
      const numpadSection = document.getElementsByClassName("numpad-section")[0];

      imageSection.style = "margin-left: -45%;";
      numpadSection.style = "left: 55%;";
    },
  },
};
</script>

<style lang="scss" scoped>
a::after {
  display: none;
}

.container {
  overflow: hidden;
}

.image-section {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.5s;

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

    .caption-1 {
      margin-left: 0.25rem;
    }

    // .input-wrapper
    div {
      margin-top: 1.25rem;
      display: flex;

      div {
        width: 20%;

        .field {
          width: 100%;
          height: 3.5rem;
          margin: 0.25rem;
          background: var(--color-white);
          border: 1px solid rgb(152, 145, 164);
          border-radius: 10px;
          text-align: center;
          font-size: 1.5rem;
        }

        .field-filled {
          width: 100%;
          height: 3.5rem;
          margin: 0.25rem;
          background: var(--color-white);
          border: 1px solid rgb(21, 21, 34);
          border-radius: 10px;
          color: rgb(21, 21, 34);
          text-align: center;
          font-family: $family-sans-serif;
          font-weight: $weight-normal;
          font-size: $size-5;
        }
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

.numpad-section {
  position: absolute;
  left: 100%;
  padding: 0.25rem;
  background: rgb(233, 231, 236);
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  transition: 0.5s;

  .numpad-button-box {
    width: calc(100% / 3);
    height: calc(100% / 4);
    padding: 0.25rem;

    .numpad-key {
      width: 100%;
      height: 100%;
      background: var(--color-white);
      border-radius: 8px;
      font-size: $size-5;
      display: flex;
      justify-content: center;
      align-items: center;

      &:active {
        background: var(--color-grey);
      }
    }
  }

  .numpad-backspace {
    position: absolute;
    bottom: 0;
    right: 0;
    width: calc(100% / 3);
    height: calc(100% / 4);
    display: flex;
    justify-content: center;
    align-items: center;

    svg {
      width: 2.75rem;
    }

    svg:focus {
      outline: none;
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

  .numpad-section {
    width: 45%;
    height: 100%;
  }
}
</style>
