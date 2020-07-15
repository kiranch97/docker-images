<template>
  <odk-container>
    <div class="image-section" aria-hidden="true">
      <img src="../assets/pwa/notification.svg" alt="Object Detection Kit abstract figure">
    </div>

    <div class="text-section">
      <h1>Clear data to continue</h1>
      <p>You have probably denied access to your GPS location or camera. As this app is a progressive web app you will have to clear the data stored to continue.</p>
      <p>
        <router-link :to="{ name:'reset-manual', params: { openCard: 'android' } }">
          How to clear stored data?
        </router-link>
      </p>
    </div>
  </odk-container>
</template>

<script>
export default {
  components: {
    OdkContainer: () => import("@/components/elements/Container.vue"),
  },
};
</script>

<style lang="scss" scoped>
.image-section {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50%;

  img {
    width: 85%;
    max-height: 426px;
    object-fit: contain;
  }
}

.text-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  padding: 0 2rem;
  height: 50%;
  min-height: 20rem;
  text-align: left;
}

@media (orientation: landscape) {
  .image-section {
    width: 45%;
    height: auto;

    img {
      transform: translate(-20%, -5%);
      width: 100%;
    }
  }

  .text-section {
    width: 55%;
    height: auto;
  }
}
</style>
