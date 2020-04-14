<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "app"
};
</script>

<style>
:root {
  --main-purple-color: #3a225d;
  --second-purple-color: #2f1c50;
  --red-color: #e1524a;
  --pink-color: #c83760;
  --yellow-color: #f6d365;
  --white-color: #ffffff;
  --second-white-color: #f9f8fa;
  --black-color: #000000;
  --dark-blue-color: #151522;
  --error-color: #c83737;
  --success-color: #37c88b;
  --grey-color: #e2dee9;
  --grey-blue-color: #9891a4;
}

/* Text styles */

.odk-title {
  font-family: "Open Sans", sans-serif !important;
  font-size: 1.25rem !important; /*20px*/
  font-weight: 700 !important;
  line-height: 2rem !important;
  color: var(--dark-blue-color) !important;
}

.title-2{
  font-family: "Open Sans", sans-serif !important;
  font-size: 1.125rem !important; /*20px*/
  font-weight: 700 !important;
  line-height: 2rem !important;
  color: var(--dark-blue-color) !important;
}

.body-1 {
  margin-top: 1rem !important;
  font-family: "Open Sans", sans-serif !important;
  font-size: 1rem !important;
  font-weight: 400 !important;
  line-height: 1.5rem !important;
  color: var(--dark-blue-color) !important;
}

.body-2 {
  /* margin-top: 1rem !important; */
  font-family: "Open Sans", sans-serif !important;
  font-size: 0.875rem !important;
  font-weight: 600 !important;
  line-height: 1.875rem !important;
  color: var(--dark-blue-color) !important;
}

.caption-1 {
  font-family: "Open Sans", sans-serif !important;
  font-size: 0.75rem !important;
  font-weight: 400 !important;
  line-height: 1.125rem !important;
  color: var(--dark-blue-color) !important;
}

/*  */

html,
body {
  background: var(--grey-color) !important;
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  /* overflow: hidden !important; */
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
}

button:focus {
  outline: none !important;
}
</style>
