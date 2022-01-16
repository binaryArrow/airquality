<template>
  <div id="dash-board">

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
  },
  mounted() {
    let width = 1000, height = 1000;
    let data = [100, 150, 200, 250, 280, 300];
    let svg = d3.select("#dash-board")
        .append("svg")
        .attr("width", width)
        .attr("height", height);


    // Erstellung der Achsen
    let xscale = d3.scaleLinear()
        .domain([0, d3.max(data) as number]) //Typecast nötig, ansonsten Error
        .range([0, width-100]);

    let yscale = d3.scaleLinear()
        .domain([0, d3.max(data) as number])
        .range([height/2, 0]);

    let x_axis = d3.axisBottom(xscale)
    let y_axis = d3.axisLeft(yscale)

    // zum Anzeigen der y-Achse
    svg.append("g")
        .attr("transform", "translate(50,10)")
        .call(y_axis);

    // zum Anzeigen der x-Achse
    let xAxisTranslate = height/2 + 10
    svg.append("g")
        .attr("transform", "translate(50, " + xAxisTranslate + ")")
        .call(x_axis)



  }
}

</script>

<style lang="scss">

</style>