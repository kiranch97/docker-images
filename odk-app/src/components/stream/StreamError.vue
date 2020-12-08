<template>
  <div id="stream-error">
    <div id="stream-error-indicator" />
    <p>{{ streamError.message }}</p>
  </div>
</template>

<script>
export default {
  name: "StreamError",

  props: {
    streamError: {
      type: Object,
      default () {
        return {
          state: false, // true = error occured
          message: null, // error message to display
          level: 1, // 1 = error, 2 = warning
        };
      },
    },
  },

  data () {
    return {
      streamErrorDiv: null,
      streamErrorIndicator: null,
    };
  },

  watch: {
    streamError (obj) {
      if (!obj.state) {
        this.streamErrorDiv.style = "display: none;";
        return;
      }

      if (obj.level === 1) {
        // Error (red (is-error))
        this.streamErrorDiv.style = "display: flex; color: rgb(200, 55, 55);";
        this.streamErrorIndicator.style = "background: rgb(200, 55, 55);";
        return;
      }

      // Warning (gold (is-warning))
      this.streamErrorDiv.style = " display: flex; color: rgb(200, 148, 55);";
      this.streamErrorIndicator.style = "background: rgb(200, 148, 55);";
    },
  },

  mounted () {
    this.streamErrorDiv = document.getElementById("stream-error");
    this.streamErrorIndicator = document.getElementById("stream-error-indicator");
  },
};
</script>

<style lang="scss" scoped>
#stream-error {
  position: absolute;
  top: 4.5rem;
  max-width: 65%;
  height: 2.5rem;
  background: var(--color-white);
  border-radius: 6px;
  color: var(--color-error);
  font-weight: $weight-semibold;
  display: none;
  justify-content: center;
  align-items: center;

  &-indicator {
    position: absolute;
    top: 0;
    left: 0;
    width: 0.5rem;
    height: 100%;
    background: var(--color-error);
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
  }

  p {
    margin: 0 1rem 0 1.5rem;
  }
}
</style>