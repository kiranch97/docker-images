<template>
  <div class="manual container">
    <header>
      <router-link to="/">
        <img class="logo" src="../../assets/manual/logo.svg">
      </router-link>
    </header>

    <main>
      <h1 class="title is-4">{{ content.title }}</h1>

      <p>{{ content.subtext }}</p>

      <b-collapse
        v-for="(manual, index) of content.manuals"
        :key="index"
        :open="accordion['isOpen'] === index"
        class="card"
        animation="fade slide"
        @open="accordion['isOpen'] = index"
      >
        <div
          slot="trigger"
          slot-scope="props"
          class="card-header"
          role="button"
        >
          <p class="card-header-title is-size-6 has-text-weight-medium">
            {{ manual.browserName }}
          </p>
          <a class="card-header-icon is-size-4">
            <div v-if="props.open">−</div>
            <div v-else>+</div>
          </a>
        </div>
        <div class="card-content">
          <div v-if="manual.steps" class="content">
            <section
              v-for="(step, sI) in manual.steps"
              :key="sI"
              class="step"
            >
              <h2 class="title is-6">{{ step.step }}</h2>
              <p>{{ step.instruction }}</p>
              <img
                :src="require(`../../assets/manual/${step.stepImage}.png`)"
                alt="step.instruction"
                class="image"
              >
            </section>
          </div>

          <div v-else class="content">
            <h2>{{ manual.attention }}</h2>
            <p>{{ manual.recommendation }}</p>
            <p>{{ manual.body }}</p>
          </div>
        </div>
      </b-collapse>
    </main>

    <footer>
      {{ content.copyright }}
    </footer>
  </div>
</template>

<script>
import content from "./content.json";

export default {
  data () {
    return {
      content,

      accordion: {
        isOpen: 0,
      },
    };
  },

  computed: {
    activeVendor () {
      return this.$route.params.activeVendor;
    },
  },

  mounted () {
    if (this.activeVendor) {
      this.accordion.isOpen = this.content.manuals.findIndex(manual => manual.sysName === this.activeVendor);
    }
  },
};
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: var(--second-white-color);
  width: 100%;
  max-width: 414px;
  height: 100%;
  min-height: calc(100vh - 1px);
  overflow-y: auto;
  text-align: left;

  @media (max-width: 1024px) and (orientation: portrait) {
    top: 0;
  }

  @media (max-width: 1024px) and (orientation: landscape) {
    top: 0;
    max-width: none;
    max-height: none;
  }
}

header {
  display: flex;
  align-items: center;
  background: var(--main-purple-color);
  width: 100%;
  height: 5rem;

  .logo {
    margin-left: 1.5rem;
    height: 24px;
  }
}

main {
  padding: 2.375rem 1.5rem;
}

footer {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--main-purple-color);
  width: 100%;
  height: 4rem;
  color: white;
}

.card {
  &-header {
    &-icon {
      div {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
      }
    }
  }
}

.step {
  margin-top: 2em;

  &:first-of-type {
    margin-top: 0;
  }
}

.image {
  border-radius: 12px;
  width: 100%;
  object-fit: contain;
}
</style>
