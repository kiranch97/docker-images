export const startupCheck = {
  methods: {
    checkAppMode () {
      const checkMedia = window.matchMedia("(display-mode: standalone)").matches;

      if (checkMedia) {
        console.log("This is running as standalone.");

        // If user installed the PWA he does not have to see this page.
        this.$router.push("/recommendation");
      } else {
        console.log("This is running in the browser");
      }
    },
  },
};
