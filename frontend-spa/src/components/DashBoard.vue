<template>
  <div id="dash-board">
      <div class="row">
        <div class="column"  id="line-chartTEMP">

        </div>
        <div class="column" id="line-chartRH">

        </div>
      </div>
      <div class="row">
        <div class="column" id="line-chartCO2">

        </div>
        <div class="column" id="line-chartTVOC">

        </div>
        <div id="Ampel">
          <div id="redCircle"></div>
          <div id="yellowCircle"></div>
          <div id="greenCircle"></div>
        </div>
      </div>
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
      axisWidth: 500,
      axisHeight: 500,
      sensorData1: [] as SensorData[],
      sensorData2: [] as SensorData[],
      sensorData3: [] as SensorData[],
      margin: {
        left: 40,
        right: 20,
        bottom: 20,
        top: 40
      },
      scales:{
        x: null,
        y: null
      }
    }
  },
  mounted() {
    this.createTEMPAxis()
    this.createRHAxis()
    this.createCO2Axis()
    this.createTVOCAxis()
  },
  methods:
      {
    // Erstellen von Random Daten (muss geändert werden..)
    create_X_Value(): number {
      let x = 0
      let returnX = 0
      for (let i=0; i<100; i++){
        returnX = x
        x++
      }
      return returnX
    },
    create_Y_Value(): number {
      let y = 0
      let returnY = 0
      for(let j=0; j<100; j++){
        returnY = y
        y++
      }
      return y
    },

    // Erstellung von Koordinatensystem
    createTEMPAxis(){

      // Erstellung und Initialisierung der Linie (funktioniert nicht bzw. Graph wird warum auch immer gar nicht angezeigt) iwo ein Denkfehler drinne
      interface graphData{
        xData: number,
        yData: number
      }

      /*
              let randomData: graphData[] = [{
              "x_Value": this.create_X_Value(),
              "y_Value": this.create_Y_Value()
            }]
      */

      let randomData: graphData[] = [{
        "yData": 0,
        "xData": 0
      }, {
        "yData": 0.2,
        "xData": 0.1
      }, {
        "yData": 0.5,
        "xData": 0.2
      }];


      let svg = d3.select("#line-chartTEMP")
          .append("svg")
          .attr("width", this.axisWidth)
          .attr("height", this.axisHeight)
          .append("g")
          .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")

      // Erstellung der Scales, fehlt noch ein D.domain für bessere Anpassung von Daten
      let xScale = d3.scaleLinear()
          .range([0, this.axisWidth - 100])

      let yScale = d3.scaleLinear()
          .range([this.axisHeight/2, 0]);


      let xAxis = d3.axisBottom(xScale)
      let yAxis = d3.axisLeft(yScale)

      svg.append("g")
          .attr("transform", "translate(0,0)")
          .call(yAxis)

      svg.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 0 - this.margin.left - 5)
          .attr("x",60 - (this.axisHeight / 2))
          .attr("dy", "1em")
          .style("font-weight", "bold")
          .text("Temperatur in °C")

      // entweder Koordinatensystem oder Linie selber bewegen und sie ans Koordinatensystem anpassen

      let xAxisTranslate = this.axisHeight/2
      svg.append("g")
          .attr("transform", "translate(0, " + xAxisTranslate + ")")
          .call(xAxis)

      svg.append("text")
          .attr("transform", "translate(200,290)")
          .style("font-weight", "bold")
          .text("Zeit")

      let line = d3.line<graphData>()
          .x(function (d){return xScale(d["xData"])})
          .y(function (d){return yScale(d["yData"])})


      svg.append("path")
          .attr("d", line(randomData))
          .attr('stroke', 'blue')
          .attr('stroke-width', 2)
          .attr('fill', 'none');

      },

    createRHAxis(){
      //
      let svg = d3.select("#line-chartRH")
          .append("svg")
          .attr("width", this.axisWidth)
          .attr("height", this.axisHeight)
          .append("g")
          .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")


      let xScale = d3.scaleLinear()
          .range([0, this.axisWidth - 100])

      let yScale = d3.scaleLinear()
          .range([this.axisHeight/2, 0]);


      let xAxis = d3.axisBottom(xScale)
      let yAxis = d3.axisLeft(yScale)

      svg.append("g")
          .attr("transform", "translate(0,0)")
          .call(yAxis)

      svg.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 0 - this.margin.left - 5)
          .attr("x",60 - (this.axisHeight / 2))
          .attr("dy", "1em")
          .style("font-weight", "bold")
          .text("Relative Feuchtigkeit (RH)")


      let xAxisTranslate = this.axisHeight/2
      svg.append("g")
          .attr("transform", "translate(0, " + xAxisTranslate + ")")
          .call(xAxis)

      svg.append("text")
          .attr("transform", "translate(200,290)")
          .style("font-weight", "bold")
          .text("Zeit")

      interface graphData{
        xData: number,
        yData: number
      }

      /*
              let randomData: graphData[] = [{
              "x_Value": this.create_X_Value(),
              "y_Value": this.create_Y_Value()
            }]
      */

      let randomData: graphData[] = [{
        "yData": 0.1,
        "xData": 0.0
      }, {
        "yData": 0.2,
        "xData": 0.1
      }, {
        "yData": 0.5,
        "xData": 0.2
      }];

      let line = d3.line<graphData>()
          .x(function (d){return xScale(d["xData"])})
          .y(function (d){return yScale(d["yData"])})

      svg.append("path")
          .attr("d", line(randomData))
          .attr('stroke', 'blue')
          .attr('stroke-width', 2)
          .attr('fill', 'none');
    },

    createCO2Axis(){
      let svg = d3.select("#line-chartCO2")
          .append("svg")
          .attr("width", this.axisWidth)
          .attr("height", this.axisHeight)
          .append("g")
          .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")


      let xScale = d3.scaleLinear()
          .range([0, this.axisWidth - 100])

      let yScale = d3.scaleLinear()
          .range([this.axisHeight/2, 0]);


      let xAxis = d3.axisBottom(xScale)
      let yAxis = d3.axisLeft(yScale)

      svg.append("g")
          .attr("transform", "translate(0,0)")
          .call(yAxis)

      svg.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 0 - this.margin.left - 5)
          .attr("x",60 - (this.axisHeight / 2))
          .attr("dy", "1em")
          .style("font-weight", "bold")
          .text("CO2-Gehalt")

      let xAxisTranslate = this.axisHeight/2
      svg.append("g")
          .attr("transform", "translate(0, " + xAxisTranslate + ")")
          .call(xAxis)

      svg.append("text")
          .attr("transform", "translate(200,290)")
          .style("font-weight", "bold")
          .text("Zeit")

    },

    createTVOCAxis(){
      let svg = d3.select("#line-chartTVOC")
          .append("svg")
          .attr("width", this.axisWidth)
          .attr("height", this.axisHeight)
          .attr("margin-top", this.margin.top)
          .attr("margin-bottom", this.margin.bottom)
          .attr("margin-left", this.margin.left)
          .attr("margin-right", this.margin.right)
          .append("g")
          .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")


      let xScale = d3.scaleLinear()
          .range([0, this.axisWidth - 100])

      let yScale = d3.scaleLinear()
          .range([this.axisHeight/2, 0]);


      let xAxis = d3.axisBottom(xScale)
      let yAxis = d3.axisLeft(yScale)

      svg.append("g")
          .attr("transform", "translate(0,0)")
          .call(yAxis)

      svg.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 0 - this.margin.left - 5)
          .attr("x",60 - (this.axisHeight / 2))
          .attr("dy", "1em")
          .style("font-weight", "bold")
          .text("TVOC-Gehalt")


      let xAxisTranslate = this.axisHeight/2
      svg.append("g")
          .attr("transform", "translate(0, " + xAxisTranslate + ")")
          .call(xAxis)

      svg.append("text")
          .attr("transform", "translate(200,290)")
          .style("font-weight", "bold")
          .text("Zeit")

    },
    }

  }
);

</script>

<style lang="scss">

#Ampel{
  position: absolute;
  bottom: 50px;
  right: 320px;
  width: 175px;
  height: 350px;
  background-color: black;
  border-radius: 25px;
}

#redCircle{
  position: absolute;
  right: 38px;
  top: 15px;
  height: 100px;
  width: 100px;
  background-color: darkred;
  border-radius: 50%;
}

#yellowCircle{
  position: absolute;
  right: 38px;
  top: 125px;
  height: 100px;
  width: 100px;
  background-color: darkgoldenrod;
  border-radius: 50%;
}

#greenCircle{
  position: absolute;
  right: 38px;
  top: 235px;
  height: 100px;
  width: 100px;
  background-color: darkgreen;
  border-radius: 50%;
}

.column{
  margin: 5px;
  display: inline-block;
  border: 3px solid black;
  height: 400px;
  box-shadow: 3px 3px 2px grey;
}

.row{
  clear: both;
  text-align: left;
  height: 410px;
}

</style>