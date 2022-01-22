<template>
  <div id="dash-board">

  </div>
</template>

<script lang="ts">
import * as d3 from 'd3'
import {defineComponent} from 'vue';
import {line, NumberValue} from "d3";

export default defineComponent({
  name: "DashBoard",
  data() {
    return {
      width: 900,
      height: 1000,
      graphData: {
        axisData: 40,
        random: d3.randomNormal(0, .2),
      },
      margin: {
        left: 40,
        right: 20,
        bottom: 20,
        top: 20
      },
      scales:{
        x: null,
        y: null
      },
    }
  },
  mounted() {

    let graph = d3.range(this.graphData.axisData).map(this.graphData.random);
    let svg = d3.select("#dash-board")
      .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)
        .attr("margin-top", this.margin.top)
        .attr("margin-bottom", this.margin.bottom)
        .attr("margin-left", this.margin.left)
        .attr("margin-right", this.margin.right)
      .append("g")
        .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")

    // Erstellung der Achsen
    let xscale = d3.scaleLinear()
        .domain([0, d3.max(graph) as number])
        .range([0, this.width-100]);

    let yscale = d3.scaleLinear()
        .domain([0, d3.max(graph) as number])
        .range([this.height/2, 0]);

    // Einspeichern der Daten
    let randomData = this.createRandomData()

    let x_axis = d3.axisBottom(xscale)
    let y_axis = d3.axisLeft(yscale)

    // zum Anzeigen der y-Achse
    svg.append("g")
        .attr("transform", "translate(50,10)")
        .call(y_axis);

    // zum Anzeigen der x-Achse
    let xAxisTranslate = this.height/2 + 10
    svg.append("g")
        .attr("transform", "translate(50, " + xAxisTranslate + ")")
        .call(x_axis)

    svg.append("path")
        .datum(randomData)
        .attr("fill", "none")
        .attr("stroke", "blue")
        .attr("stroke-width", 1.5)

    let line = d3.line() // Irgendwie das hier zum laufen bringen


  },
  methods: {
    // Erstellen von Random Daten
    createRandomData() {
      let getData = function (){
        let data = []
        for(let i=0; i<100; i++){
          data.push({
            x: i,
            y: Math.round(Math.random()*100)
          })
        }
      }
      return getData
    },

    tick() {
      //let message = "Hello World"

    }
  }
});

</script>

<style lang="scss">

</style>