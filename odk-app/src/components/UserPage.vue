<template>
  <odk-container>
    <div class="image-section">
      <img src="../assets/pwa/intro.png" alt>
    </div>

    <div class="text-section">
      <div class="text-section-header">
        <h1 class="odk-title is-4 page-title">
          <router-link to="/welcome">
            <img
              svg-inline
              svg-sprite
              src="@/assets/ui/chevron-left.svg"
              alt="Ga terug"
              class="back-button"
            >
          </router-link>
          Inloggen
        </h1>
        <p class="caption-1">Deze login is voor medewerkers van Gemeente Amsterdam.</p>
      </div>

      <div class="text-section-dropdown">
        <b-field label="Scan-chauffeur">
          <b-select v-model="chosenDriver" class="select" placeholder="Selecteer uw ID">
            <option
              v-for="option in drivers"
              :key="option.id"
              :value="option.name"
            >
              {{ option.name }}
            </option>
          </b-select>
        </b-field>

        <img src="../assets/pwa/gemeente-logo.png" alt>
      </div>
    </div>
  </odk-container>
</template>

<script>
export default {
  name: "UserPage",

  data () {
    return {
      chosenDriver: null,
      drivers: [
        {
          name: "AG001",
        },
        {
          name: "AG002",
        },
        {
          name: "AG003",
        },
      ],
    };
  },

  watch: {
    chosenDriver (value) {
      console.log(value);
      if (value != null) {
        setTimeout(() => {
          this.$router.push({
            name: "code-page",
            params: { username: value },
          });
        }, 200);
      }
    },
  },

  mounted () {},

  methods: {},
};
</script>

<style lang="scss" scoped>
a::after {
  display: none;
}

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
  }

  &-dropdown {
    width: 100%;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;

    .field {
      width: 100%;
      text-align: left;

      ::v-deep .label {
        font-weight: 600;
      }

      .control {
        width: 100%;

        &::after {
          display: none;
        }

        ::v-deep span {
          width: 100%;

          &::after {
            border-color: var(--color-black);
          }

          select {
            width: 100%;
            border: 1px solid rgb(152, 145, 164);

            &:active,
            &:focus {
              box-shadow: none;
            }
          }
        }
      }
    }

    img {
      width: 30%;
      margin-top: 1rem;
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