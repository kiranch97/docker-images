<template>
  <div :class="[$style['manual'], 'container']">
    <header :class="$style['manual-header']">
      <router-link to="/">
        <img :class="$style['manual-header-logo']" src="../../assets/manual/logo.svg">
      </router-link>
    </header>

    <main :class="$style['manual-body']">
      <div class="content">
        <h1 class="title is-4">{{ content.title }}</h1>

        <p>{{ content.subtext }}</p>
      </div>

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
          <a class="card-header-icon is-size-3">
            <div
              v-if="props.open"
              :class="$style['icon-collapse']"
            >
              −
            </div>
            <div
              v-else
              :class="$style['icon-collapse']"
            >
              +
            </div>
          </a>
        </div>
        <div class="card-content">
          <div v-if="manual.steps" class="content">
            <section
              v-for="(step, sI) in manual.steps"
              :key="sI"
              :class="$style['manual-step']"
            >
              <h2 class="title is-5">{{ step.step }}</h2>
              <p>{{ step.instruction }}</p>
              <img
                :src="require(`../../assets/manual/${step.stepImage}.png`)"
                alt="step.instruction"
                :class="$style['manual-image']"
              >
            </section>
          </div>

          <div v-else class="content">
            <h2 class="title is-6">{{ manual.attention }}</h2>
            <p><strong class="has-text-weight-medium">{{ manual.recommendation }}</strong></p>
            <p>{{ manual.body }}</p>
          </div>
        </div>
      </b-collapse>
    </main>

    <footer :class="$style['manual-footer']">
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
  background: white;
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

.card {
  margin: 0.5rem auto;
  box-shadow: none;
  background-color: var(--second-white-color);

  &-header {
    box-shadow: none;
  }
}
</style>

<style lang="scss" module>
.manual {
  &-header {
    display: flex;
    flex: 0 1 auto;
    align-items: center;
    background: var(--main-purple-color);
    width: 100%;
    height: 5rem;

    &-logo {
      margin-left: 1.5rem;
      height: 24px;
    }
  }

  &-body {
    flex: 1 1 100%;
    padding: 2.375rem 1.5rem;
  }

  &-step {
    margin-top: 2em;

    &:first-of-type {
      margin-top: 0;
    }
  }

  &-image {
    border-radius: 12px;
    width: 100%;
    object-fit: contain;
  }

  &-footer {
    display: flex;
    flex: 0 1 auto;
    align-items: center;
    justify-content: center;
    background: var(--main-purple-color);
    width: 100%;
    height: 4rem;
    color: white;
  }
}

.icon-collapse {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
  color: black;
}
</style>
