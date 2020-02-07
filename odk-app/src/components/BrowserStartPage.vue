<template>
  <div id="container">
    <div id="image-section">
      <img id="intro-img" src="../assets/pwa/intro.png" alt />
    </div>
    <div id="text-section">
      <p class="odk-title" id="title">Object Detection Kit</p>
      <p class="body-1">Keep streets clean by scanning garbage while driving</p>
      <p class="body-1">
        Please
        <span id="add-to-home">‘add to homescreen’</span> to continue
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "browser-startpage",
  data() {
    return {};
  },
  methods: {
      checkAppMode(){
            if (window.matchMedia("(display-mode: standalone)").matches) {
            console.log("This is running as standalone.");
            this.$router.push({ path: "/pwa" });
            }else {
                console.log("This is running on the browser")
            }
        }
 },
  mounted() {
      this.checkAppMode()
  }
    
};
</script>

<style scoped>
.odk-title {
  font-size: 1.5rem;
  font-weight: 800;
  line-height: 2.125rem;
  color: var(--dark-blue-color);
  margin-bottom: 0.75rem;
  
}

.body-1 {
  font-family: "Open Sans", sans-serif;
  font-size: 1rem;
  font-weight: 400;
  line-height: 26px;
  color: var(--dark-blue-color);
  width: 15rem;
}

#container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  justify-content: center;
  align-items: center;
  max-height: 800px;
  max-width: 500px;
  margin: 0 auto;
  position: relative;
  top: 3rem; 
}

#container div {
  background: var(--second-white-color);
  width: 100%;
  height: 100%;
}

#text-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 20rem;
}

#text-section :nth-child(2) {
  margin-bottom: 5rem;
}

#add-to-home {
  font-weight: 700;
}

#image-section {
  display: flex;
  justify-content: center;
  align-items: center;
}

#intro-img {
  max-height: 320px;
  object-fit: cover;
  position: relative;
  right: 2rem;
}

@media (max-width: 1024px) and (orientation: portrait) {
  #container div {
    background: var(--second-white-color);
    width: 100%;
    height: 100%;
  }

  #container{
    top: 0;
  }

  #image-section {
    display: flex;
    justify-content: flex-start;
  }
}

@media (max-width: 1024px) and (orientation: landscape) {
  #container {
    flex-direction: row;
    top: 0;
    max-width: none;
    max-height: none;
  }
}
</style>