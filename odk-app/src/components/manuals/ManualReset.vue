<template>
  <manual
    :content="content"
    :open-card="openCard"
  />
</template>

<script>
import content from "./contentResetManual.json";

export default {
  name: "InstallManual",

  components: {
    Manual: () => import("./Manual"),
  },

  data () {
    return {
      content,
    };
  },

  computed: {
    openCard () {
      return this.$route.params.openCard;
    },
  },
};
</script>
