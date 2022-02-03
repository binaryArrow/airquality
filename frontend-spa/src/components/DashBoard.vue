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
      </div>
  </div>
</template>

<script lang="ts">
import * as d3 from 'd3'
import {defineComponent} from 'vue';
import {SensorData} from "@/../../backend/src/models/SensorData";
import {io} from "socket.io-client";
import {Communicator} from "@/service/communicator";

const socket = io("http://localhost:3000")

export default defineComponent({
  name: "DashBoard",
  data() {
    return {
      axisWidth: 500,
      axisHeight: 500,
      sensorData1: [] as SensorData[],
      sensorData2: [] as SensorData[],
      sensorData3: [] as SensorData[],
      communicator: new Communicator(),
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

    // Funktion von Can für Empfang von Sensordaten (reicht das schon?)
    this.communicator.getSensorData(1, 50)
    this.communicator.getSensorData(2, 50)
    this.communicator.getSensorData(3, 50)

    // Socket für Datenübertragung (einfach von Sketchingboard übernehmen?)
    socket.on("data", (data: SensorData) => {
        const allSensorData = new SensorData(data.sensorId, data.tempSHT21, data.humSHT21, data.tempSCD41, data.humSCD41, data.co2SCD41, data.eco2CCS811, data.tvocCCS811.trim())
      switch (allSensorData.sensorId){
        case 1:{
          this.sensorData1.push(allSensorData)
          break;
        }
        case 2:{
          this.sensorData2.push(allSensorData)
          break;
        }
        case 3:{
          this.sensorData3.push(allSensorData)
          break;
        }
      }
    })

    this.createTEMPAxis()
    this.createRHAxis()
    this.createCO2Axis()
    this.createTVOCAxis()
  },
  methods:
      {
    createTEMPAxis(){

      interface graphData{
        xDate: number, // muss evtl. zu Date geändert werden, x-Achse ist für Zeit (ist xData überhaupt nötig?)
        yTempSHT?: number // tempSHT21 ist eig ein String, aber deswegen macht line()-Funktion macht Probleme
        yTempSCD?: number
      }

      let randomData: graphData[] = [{
        xDate: Date.now(),
        yTempSHT: 20 // wie übernimmt man SensorData von den beiden Sensoren??? (zwei verschiedene Möglichekeiten einbauen(switch_case?)
      }];

      let svg = d3.select("#line-chartTEMP")
          .append("svg")
          .attr("width", this.axisWidth)
          .attr("height", this.axisHeight - 100)
          .append("g")
          .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")


      let xScale = d3.scaleTime()
          .range([0, this.axisWidth - 100])

      do{
        xScale.domain([Date.now() - (50 * 1000) / 2, Date.now() + (50 * 1000) / 2])
      }while(!stop);


      let yScale = d3.scaleLinear()
          .range([this.axisHeight/2, 0])
          .domain([0, 60])


      let xAxis = d3.axisBottom(xScale)
          .ticks(d3.timeSecond.every(10)) // sorgt für die 10 Sekunden Abstände

      let yAxis = d3.axisLeft(yScale)

      // y-Achse wird aufgerufen
      svg.append("g")
          .attr("transform", "translate(0,0)")
          .call(yAxis)

      svg.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 0 - this.margin.left - 5)
          .attr("x",60 - (this.axisHeight / 2))
          .attr("dy", "1em")
          .style("font-weight", "bold")
          .text("Temperatur (°C)")

      // x-Achse wird aufgerufen
      let xAxisTranslate = this.axisHeight/2
      svg.append("g")
          .attr("transform", "translate(0, " + xAxisTranslate + ")")
          .transition()
          .duration(500)
          .ease(d3.easeLinear)
          .call(xAxis)


      svg.append("text")
          .attr("transform", "translate(200,290)")
          .style("font-weight", "bold")
          .text("Zeit")

      let line = d3.line<graphData>()
          .x(function (d){return xScale(d["xDate"])})
          .y(function (d){return yScale(d["yTempSHT"])}) // wieder hier der Fehler


      svg.append("path")
          .attr("d", line(randomData))
          .attr("stroke", "orange")
          .attr("stroke-width", 2)
          .attr("fill", "none");

      },

    createRHAxis(){
      //
      let svg = d3.select("#line-chartRH")
          .append("svg")
          .attr("width", this.axisWidth)
          .attr("height", this.axisHeight - 100)
          .append("g")
          .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")


      let xScale = d3.scaleLinear()
          .range([0, this.axisWidth - 100])

      let yScale = d3.scaleLinear()
          .range([this.axisHeight/2, 0])
          .domain([0, 100])


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
          .text("Relative Feuchtigkeit (%)")


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

      let randomData: graphData[] = [{
        "yData": 50,
        "xData": 0.0
      }, {
        "yData": 20,
        "xData": 0.1
      }, {
        "yData": 30,
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
          .attr("height", this.axisHeight - 100)
          .append("g")
          .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")


      let xScale = d3.scaleLinear()
          .range([0, this.axisWidth - 100])

      let yScale = d3.scaleLinear()
          .range([this.axisHeight/2, 0])
          .domain([400, 5000])


      let xAxis = d3.axisBottom(xScale)
      let yAxis = d3.axisLeft(yScale)

      svg.append("g")
          .attr("transform", "translate(0,0)")
          .call(yAxis)

      svg.append("text")
          .attr("y", 0 - this.margin.left + 10)
          .attr("dy", "1em")
          .style("font-weight", "bold")
          .text("CO2-Gehalt (ppm)")

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
          .attr("height", this.axisHeight - 100)
          .append("g")
          .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")


      let xScale = d3.scaleLinear()
          .range([0, this.axisWidth - 100])

      let yScale = d3.scaleLinear()
          .range([this.axisHeight/2, 0])
          .domain([0, 1200])


      let xAxis = d3.axisBottom(xScale)
      let yAxis = d3.axisLeft(yScale)

      svg.append("g")
          .attr("transform", "translate(0,0)")
          .call(yAxis)

      svg.append("text")
          .attr("y", 0 - this.margin.left + 10)
          .attr("dy", "1em")
          .style("font-weight", "bold")
          .text("TVOC-Gehalt (ppb)")


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


#line-chartTEMP{
  position: relative;
  float: left;
}

#line-chartCO2{
  position: relative;
  float: left;
}


.column{
  margin: 5px;
  display: inline-block;
  border: 3px solid black;
  height: 400px;
  box-shadow: 3px 3px 2px grey;
  border-radius: 20px;
}

.row{
  clear: both;
  text-align: left;
  height: 410px;
}


</style>