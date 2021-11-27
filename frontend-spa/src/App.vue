<template>
  <h1>Airquality-App</h1>
  <div id="nav">
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </div>
  <router-view/>
</template>

<style lang="scss">
/*
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
*/
#nav {
  text-align: center;
  padding: 30px;
  a {
    font-weight: bold;
    color: #000000;

    &.router-link-exact-active {
      color: #85782b;
    }
  }
}
</style>
