<template>
  <manual
    :content="content"
    :open-card="openCard"
    :scroll-to-card="true"
  />
</template>

<script>
import content from "./contentInstallManual.json";

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
