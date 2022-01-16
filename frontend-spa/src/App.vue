<template>
  <div class="app-name">
    <h1><b>Airquality-App</b></h1>
  </div>
  <div id="nav">
    <router-link to="/">Home</router-link>
    |
    <router-link to="/about">Dashboard</router-link>
  </div>
  <router-view/>
</template>

<style lang="scss">
.app-name {
  background: #ece6d9;
  text-align: center;
  font-size: xx-large;
  border: 2px solid black;
}
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
