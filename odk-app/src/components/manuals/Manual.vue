<template>
  <odk-container
    direction="column"
    bg-color="white"
    :fullheight="false"
    :fullwidth="true"
    :class="$style['manual']"
  >
    <header :class="$style['manual-header']">
      <img
        :class="$style['manual-header-logo']"
        src="../../assets/manual/logo.svg"
        @click="goBack"
      >
    </header>

    <main :class="$style['manual-body']">
      <div class="content">
        <h1 class="title is-4" :class="$style['page-title']">
          <router-link to="/">
            <img
              svg-inline
              svg-sprite
              src="@/assets/ui/chevron-left.svg"
              alt="Ga terug"
              :class="$style['back-button']"
            >
          </router-link>
          {{ content.title }}
        </h1>

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
          <p
            :data-sys-name="manual.sysName"
            class="card-header-title is-size-6 has-text-weight-medium"
          >
            {{ manual.cardTitle }}
          </p>
          <a class="card-header-icon is-size-3 no-anim">
            <div
              :class="$style['icon-collapse']"
            >
              <template v-if="props.open">
                −
              </template>
              <template v-else>
                +
              </template>
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
              <component-includer
                v-for="(component, cIndex) in step.components"
                :key="cIndex"
                :component-data="component"
              >
                {{ component.cContent }}
              </component-includer>
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
  </odk-container>
</template>

<script>
export default {
  name: "Manual",

  components: {
    ComponentIncluder: () => import("@/components/util/ComponentIncluder.vue"),
  },

  props: {
    content: {
      type: Object,
      default: () => {},
    },
    openCard: {
      type: String,
      default: null,
    },
    scrollToCard: {
      type: Boolean,
      default: false,
    },
  },

  data () {
    return {
      accordion: {
        isOpen: 0,
      },
    };
  },

  mounted () {
    if (this.openCard) {
      const scrollOptions = {
        easing: "ease-in",
        offset: -50,
        force: true,
        cancelable: true,
      };

      this.accordion.isOpen = this.content.manuals.findIndex(manual => manual.sysName === this.openCard);

      if (this.scrollToCard) {
        this.$scrollTo(this.$el.querySelector(`[data-sys-name="${[this.content.manuals[this.accordion.isOpen].sysName]}"]`), 250, scrollOptions);
      }
    }
  },

  methods: {
    goBack () {
      this.router.back();
    },
  },
};
</script>

<style lang="scss" scoped>
.card {
  margin: 0.75rem auto;
  border-radius: 6px;
  box-shadow: none;
  background-color: var(--color-white-bis);

  &-header {
    box-shadow: none;
    height: 54px;

    &-icon {
      padding-top: 0;
      padding-bottom: 0;
    }

    &-title {
      margin: 0;
      padding-top: 0;
      padding-bottom: 0;
    }
  }
}

.manual-image {
  border-radius: 12px;
  width: 100%;
  object-fit: contain;
}
</style>

<style lang="scss" module>
.manual {
  text-align: left;

  &-header {
    display: flex;
    flex: 0 1 auto;
    align-items: center;
    background: var(--color-purple);
    width: 100%;
    min-height: 4rem;

    &-logo {
      margin-left: 1.5rem;
      height: 24px;
    }
  }

  &-body {
    flex: 1 1 100%;
    align-self: center;
    padding: 2.375rem 1rem;
    width: 100%;
    max-width: 414px;
  }

  &-step {
    margin-top: 2em;

    &:first-of-type {
      margin-top: 0;
    }
  }

  &-footer {
    display: flex;
    flex: 0 1 auto;
    align-items: center;
    justify-content: center;
    background: var(--color-purple);
    width: 100%;
    min-height: 4rem;
    color: white;
  }
}

.page-title {
  display: flex;

  .back-button {
    margin-right: 1rem;
    width: 1.675rem;
    height: 1.675rem;
    outline: none;
  }
}

.icon-collapse {
  display: flex;
  align-items: center;
  justify-content: center;
  transform: translateY(-2px);
  width: 1.675rem;
  height: 1.675rem;
  text-align: center;
  color: black;
  font-size: 1.1em;
}
</style>
