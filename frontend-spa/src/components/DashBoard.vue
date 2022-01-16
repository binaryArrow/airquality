<template>
  <div class="dash-board">
    <svg :class="axes">
      <line stroke-width="20px"/>
    </svg>
  </div>
</template>

<script lang="ts">
import * as d3 from 'd3'

export default {
  name: "DashBoard",
  data(){
    return{
      width: 1200,
      height: 600,
      margin: {
        left: 20,
        right: 10,
        bottom: 10,
        top: 20
      },
      scales:{
        x: null,
        y: null
      }
    }
  }
}


</script>

<style lang="scss">

</style>