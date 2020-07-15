<template>
  <component
    :is="element"
    :class="[ 'container', ...classes ]"
  >
    <slot />
  </component>
</template>

<script>
export default {
  name: "OdkContainer",

  props: {
    /**
     * The HTML element name used for the container.
     */
    element: {
      type: String,
      default: "div",
      validator: value => value.match(/(div|article|aside|ul|ol|header|section|footer|span)/),
    },

    /**
     * Whether the container spans the full width of the window.
     */
    fullwidth: {
      type: Boolean,
      default: false,
    },

    /**
     * Whether the container spans the viewport vertically.
     */
    fullheight: {
      type: Boolean,
      default: true,
    },

    /**
     * How the container is positioned in the layout with CSS.
     */
    position: {
      type: String,
      default: null,
      validator: value => value === null || value.match(/(relative)/),
    },

    /**
     * Flex direction of the container.
     */
    direction: {
      type: String,
      default: null,
      validator: value => value === null || value.match(/(row|column)/),
    },

    /**
     * Flex alignment (cross-axis) of children of the container.
     */
    align: {
      type: String,
      default: null,
      validator: value => value === null || value.match(/(center|space-around|space-between|start|end)/),
    },

    /**
     * Flex justification (main-axis) of children of the container.
     */
    justify: {
      type: String,
      default: null,
      validator: value => value === null || value.match(/(center|space-around|space-between|start|end)/),
    },


    /**
     * Background colour of the container.
     */
    bgColor: {
      type: String,
      default: null,
      validator: value => value === null || value.match(/(white|white-bis|grey-light|grey)/),
    },
  },

  computed: {
    classes () {
      return [
        this.fullwidth ? "is-fluid" : null,
        this.fullheight ? "is-fullheight" : null,
        this.position ? `is-${this.position}` : null,
        this.direction ? `is-${this.direction}` : null,
        this.align ? `align-${this.align}` : null,
        this.justify ? `justify-${this.justify}` : null,
        this.bgColor ? `is-${this.bgColor}` : null,
      ];
    },
  },
};
</script>

<style lang="scss" scoped>
// `.container` class is inherited from Bulma.
.container {
  display: flex;
  transition:
    transform 250ms ease,
    width 250ms ease,
    height 250ms ease,
  ;
  margin: 0 auto;

  @media (orientation: portrait) {
    &:not(.is-fluid) {
      max-width: 414px;
    }

    &:not(.is-row) {
      flex-direction: column;
    }
  }

  @media (orientation: landscape) {
    &:not(.is-fluid) {
      max-width: 896px;
    }
  }
}
</style>
