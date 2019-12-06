<template>
  <div>
    <section class="details-box">
      <div class="feedback-line"></div>
      <div class="details-box-container">
        <div class="flex-row">
          <div class="images-row">
          <transition appear>
            <div :class="{ check: idIsActive, error: idHasError }"></div>
          </transition>
            <div :class="{ check: moduleIsActive, error: moduleHasError }"></div>
            <div :class="{ check: resoIsActive, error: resoHasError }"></div>
            <div :class="{ check: imageCountIsActive, error: imageCountNotActive }"></div>
          </div>
        </div>
        <div class="flex-row2">
          <ul class="detail-list">
            <li class="item">Device id</li>
            <p class="results">{{ myId }}</p>
            <li class="item">Module</li>
            <p class="results">No module Yet</p>
            <li class="item">Resolution</li>
            <p class="results">{{ height }} x {{ width }}</p>
            <li class="item">Frames Taken</li>
            <p class="results">{{ imageCount }}</p>
          </ul>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
export default {
  data: function() {
    return {
      myId: "",

      // -------STREAM LIST TOGGLES---------\\
      isActive: true,
      hasError: false,
      idIsActive: true,
      idHasError: false,
      moduleIsActive: false,
      moduleHasError: true,
      resoIsActive: false,
      resoHasError: false,
      imageCountIsActive: false,
      imageCountNotActive: true
    };
  },

  // ---- Receiving Props ------\\

  props: ["height", "width", "imageCount"],

  // ---- Methods ------\\

  methods: {
    loadStorageId() {
      this.myId = localStorage.deviceId;
      console.log(this.myId);
    },

    checkStreamDetaills() {
      //Check for DEVICE ID
      if (
        typeof localStorage.deviceId == "undefined" ||
        localStorage.deviceId == null
      ) {
        this.idIsActive = false;
        this.idHasError = true;
      } else {
        this.idIsActive = true;
        this.idHasError = false;
      }
      //Check for Image count
      if (this.imageCount > 0) {
        this.imageCountIsActive = true;
        this.imageCountNotActive = false;
      }
      //Check for Resolution
      if (this.height > 0 || this.width > 0) {
        this.resoIsActive = true;
        this.resoHasError = false;
      } else {
        this.resoIsActive = false;
        this.resoHasError = true;
      }
    }
  },

  // ---- On mount hook ------\\
  mounted() {
    eventBus.$on("idIsSaved", deviceId => {
      this.myId = deviceId;
    });

    this.loadStorageId();
  },

  // ---- Before update hook ------\\
  beforeUpdate() {
    this.checkStreamDetaills();
  }
};
</script>



<style scoped>
body {
  margin: 0;
}

.report-box {
  width: 50px;
  height: 50px;
  border-radius: 15%;
  background: lightgrey;
}

.item {
  font-weight: bold;
}

.details-box {
  height: 16rem;
  width: 15rem;
  background: lightgrey;
  transition: 0.2s;
  display: grid;
  grid-auto-rows: 3% 97%;
  border-radius: 3%;
}

button:first-child {
  display: flex;
  justify-content: center;
  align-content: center;
}

li:first-child {
  margin-top: 4px;
}

li:nth-child(1) {
  margin-top: 4.5px;
}
li:nth-child(2) {
  margin-top: 4.5px;
}
li:nth-child(3) {
  margin-top: 4.5px;
}
li:nth-child(4) {
  margin-top: 4.5px;
}
li:last-child {
  margin-top: 4.5px;
}



.feedback-line {
  width: 100%;
  background: #48cc55;
   border-radius: 3%;
}

.item {
  text-align: left;
}

.details-box-container {
  display: flex;
}

.flex-row {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding-left: 20px;
}

.flex-row2 {
  display: flex;
  height: 100%;
  width: 100%;
  padding-left: 20px;
}

.images-row {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 85%;
}

.check {
  background-image: url("../assets/check.png");
  background-repeat: no-repeat;
  height: 20px;
  width: 20px;
  background-size: 100% 100%;
}

.error {
  background-image: url("../assets/error.png");
  background-repeat: no-repeat;
  height: 20px;
  width: 20px;
  background-size: 100% 100%;
}

.detail-list {
  list-style-type: none;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 85%;
}

.results {
  text-align: left;
}

@keyframes fade-in {
  from {
    opacity: 0%;
  }
  to {
    opacity: 100%;
  }
}



@media (max-width: 812px) and (orientation: landscape) {
  .details-box {
    transform: rotate(90deg);
  }
}
</style>