<template>
  <div id="stream-error">
    <p>{{ streamErrorMessage }}</p>
  </div>
</template>

<script>
export default {
  name: "StreamError",

  props: {
    streamErrorMessage: {
      type: String,
      default: "Fout opgetreden! (418)",
    },
  },
};
</script>

<style lang="scss" scoped>
#stream-error {
  position: absolute;
  top: 4.5rem;
  width: 18rem;
  height: 2.5rem;
  background: var(--color-white);
  border-radius: 6px;
  color: var(--color-error);
  font-weight: $weight-semibold;
  display: flex;
  justify-content: center;
  align-items: center;

  &::before {
    position: absolute;
    top: 0;
    left: 0;
    width: 0.5rem;
    height: 100%;
    background: var(--color-error);
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
    content: "";
  }

  p {
    margin: 0 0 0 0.5rem;
  }
}
</style>