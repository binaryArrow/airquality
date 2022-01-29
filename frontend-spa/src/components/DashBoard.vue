<template>
  <div id="dash-board">
    <body id="line-chart">

    </body>
  </div>
</template>

<script lang="ts">
import * as d3 from 'd3'
import {defineComponent} from 'vue';
import {SensorData} from "@/../../backend/src/models/SensorData";

export default defineComponent({
  name: "DashBoard",
  data() {
    return {
      width: 900,
      height: 1000,
      axisRange: 100,
      sensorData1: [] as SensorData[],
      sensorData2: [] as SensorData[],
      sensorData3: [] as SensorData[],
      margin: {
        left: 40,
        right: 20,
        bottom: 20,
        top: 20
      },
      scales:{
        x: null,
        y: null
      }
    }
  },
  mounted() {
    this.createAxes()


  },
  methods: {

    // Erstellen von Random Daten
    create_X_Value(): number {
      let x = 0
      for (let i=0; i<100; i++){
        x++
      }
      return x
    },
    create_Y_Value(): number {
      let y = 0
      for(let j=0; j<100; j++){
        //y = Math.round(Math.random()*10)
        y++
      }
      return y
    },

    // Erstellung von Koordinatensystem
    createAxes(){

      let axisData = d3.range(this.axisRange) // range gibt ein Array mit bestimmten Abständen zurück

      let svg = d3.select("#line-chart")
          .append("svg")
          .attr("width", this.width)
          .attr("height", this.height)
          .attr("margin-top", this.margin.top)
          .attr("margin-bottom", this.margin.bottom)
          .attr("margin-left", this.margin.left)
          .attr("margin-right", this.margin.right)
          .append("g")
          .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")


      let xScale = d3.scaleLinear()
          .domain([0, d3.max(axisData) as number])
          .range([0, this.width - 100])

      let yScale = d3.scaleLinear()
          .domain([0, d3.max(axisData) as number])
          .range([this.height/2, 0]);


      let xAxis = d3.axisBottom(xScale)
      let yAxis = d3.axisLeft(yScale)

      svg.append("g")
          .attr("transform", "translate(50,10)")
          .call(yAxis)


      let xAxisTranslate = this.height/2 + 10
      svg.append("g")
          .attr("transform", "translate(50, " + xAxisTranslate + ")")
          .call(xAxis)

      // Erstellung und Initialisierung der Linie (funktioniert nicht bzw. Graph wird warum auch immer gar nicht angezeigt) iwo ein Denkfehler drinne
      interface graphData{
        x_Value: number,
        y_Value: number
      }

      let randomData: graphData[] = [{
        "x_Value": this.create_X_Value(),
        "y_Value": this.create_Y_Value()
      }]

      let line = d3.line<graphData>()
          .x(function (d){return xScale(d["x_Value"])})
          .y(function (d){return yScale(d["y_Value"])})

      svg.append('path')
          .datum(randomData)
          .attr('class', 'line')
          .attr('d', line(randomData));

    },

  }
});

</script>

<style lang="scss">


</style>