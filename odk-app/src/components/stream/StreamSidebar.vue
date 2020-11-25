<template>
  <div id="stream-sidebar">
    <div id="stream-sidebar-header">
      <img
        svg-inline
        src="@/assets/ui/chevron-left.svg"
        alt="Menu sluiten"
        @click="hideSidebar()"
      >
      <p>Terug</p>
    </div>

    <!-- Default options -->
    <div
      v-if="!showManualOptions"
      class="stream-sidebar-option"
      @click="showManual()"
    >
      <img svg-inline src="@/assets/ui/manual.svg" alt="Handleiding">
      <p>Handleiding</p>
      <img
        svg-inline
        src="@/assets/ui/chevron-right-grey.svg"
        alt="Naar handleiding"
        class="stream-sidebar-option-arrow"
      >
    </div>

    <div
      v-if="!showManualOptions"
      class="stream-sidebar-option"
      @click="logout()"
    >
      <img svg-inline src="@/assets/ui/logout.svg" alt="Uitloggen">
      <p>Uitloggen</p>
    </div>

    <!-- Manual options -->
    <div
      v-if="showManualOptions"
      class="stream-sidebar-option"
      @click="toManual('reset-manual')"
    >
      <img svg-inline src="@/assets/ui/manual.svg" alt="Verwijder gegevens">
      <p>Verwijder gegevens</p>
    </div>

    <div
      v-if="showManualOptions"
      class="stream-sidebar-option"
      @click="toManual('installation-manual')"
    >
      <img svg-inline src="@/assets/ui/manual.svg" alt="Installeer PWA">
      <p>Installeer PWA</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "StreamSidebar",

  data () {
    return {
      showManualOptions: false,
    };
  },

  methods: {
    hideSidebar () {
      document.getElementById("stream-sidebar").style = "left: 100%;";
      this.showManualOptions = false;
    },

    // ----

    showManual () {
      this.showManualOptions = true;
    },

    // ----

    toManual (page) {
      this.$router.push(`/${page}`);
    },

    // ----

    logout () {
      localStorage.clear();
      this.$router.push("/welcome");
    },
  },
};
</script>

<style lang="scss" scoped>
#stream-sidebar {
  position: absolute;
  left: 100%;
  width: calc(100% / 3);
  height: 100%;
  background: var(--color-white);
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
  display: flex;
  flex-direction: column;
  transition: 0.5s;
  z-index: 10;

  &-header {
    height: 2rem;
    margin: 1.25rem 0;
    display: flex;
    align-items: center;

    svg {
      width: 1.25rem;
      margin: 0 0.75rem 0 1rem;
      outline: none;
    }

    p {
      margin: 0;
      font-weight: 600;
    }
  }

  .stream-sidebar-option {
    position: relative;
    height: 2.75rem;
    display: flex;
    align-items: center;

    &:active {
      background: rgb(226, 222, 233);
    }

    svg:first-of-type {
      width: 1.25rem;
      margin: 0 0.75rem 0 1rem;
      outline: none;
    }

    p {
      margin: 0;
    }

    &-arrow {
      position: absolute;
      right: 1rem;
      outline: none;
    }
  }
}
</style>