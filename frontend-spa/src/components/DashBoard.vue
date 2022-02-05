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

    // Socket für Datenübertragung (das von SketchingBoard, fehlt noch setInterval Funktion, für 10-Sekunden Abstand)
    socket.on("data", (data: SensorData) => {
      console.log(`Daten sind angekommen von ${data.sensorId}`)
        const allSensorData = new SensorData(data.sensorId, data.tempSHT21, data.humSHT21, data.tempSCD41, data.humSCD41, data.co2SCD41, data.eco2CCS811, data.tvocCCS811.trim(), data.battery)
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
    decideTEMP(){
      let tempSHT: number
      let tempSCD: number
      const dummyObject1 = this.sensorData1[this.sensorData1.length - 1]
      const dummyObject2 = this.sensorData3[this.sensorData3.length - 1]
      tempSHT =+ dummyObject1.tempSHT21
      tempSCD =+ dummyObject2.tempSCD41
      return [tempSHT, tempSCD]
    },

    decideHUM(){
      let humSHT: number
      let humSCD: number
      const dummyObject1 = this.sensorData1[this.sensorData1.length - 1]
      const dummyObject2 = this.sensorData3[this.sensorData3.length - 1]
      humSHT =+ dummyObject1.humSHT21
      humSCD =+ dummyObject2.humSCD41
      return [humSHT, humSCD]
    },

    decideCO2(){
      let co2SCD: number
      let eco2CCS: number
      const dummyObject1 = this.sensorData1[this.sensorData1.length - 1]
      const dummyObject2 = this.sensorData3[this.sensorData3.length - 1]
      co2SCD =+ dummyObject1.co2SCD41
      eco2CCS =+ dummyObject2.eco2CCS811
      return [co2SCD, eco2CCS]
    },

    // das wird die Funktion zur Bewegung des Graphen
    updateGraph(){
      //

    },

    createTEMPAxis(){

     // var tempSHT = d3.map(this.decideTEMP()[0], function(d){return d.tempSHT21}) --> map() Method funktioniert so nicht...

      interface graphTempData{
        xDate: number // muss evtl. zu Date geändert werden, x-Achse ist für Zeit (ist xData überhaupt nötig?)
        yTempSHT: number
      }

      let tempSensorData: graphTempData[] = [{
        xDate: Date.now() + (50 * 1000) / 2,
        yTempSHT: 20}, // this.decideTEMP()[0] wenn der Wert genommen wird, verschwinden alles Graphen :D
        {
          yTempSHT: 40,
          xDate: Date.now() + (50 * 1000) / 2,
        }];

      let svg = d3.select("#line-chartTEMP")
          .append("svg")
          .attr("width", this.axisWidth)
          .attr("height", this.axisHeight - 100)
          .append("g")
          .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")

      let xScale = d3.scaleTime()
          .range([0, this.axisWidth - 100]) // das hier stimmt soweit

      // hier durch erneuert sich die x-Achse
      do{
        xScale.domain([Date.now() - (50 * 1000) / 2, Date.now() + (50 * 1000) / 2])
      }while(!stop);

      let yScale = d3.scaleLinear()
          .range([this.axisHeight/2, 0])
          .domain([0, 60]) // hier kann eine feste Domain bleiben

      let xAxis = d3.axisBottom(xScale)
          .ticks(d3.timeSecond.every(10)) // sorgt für die 10 Sekunden Abstände auf Achse

      let yAxis = d3.axisLeft(yScale)

      svg.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 0 - this.margin.left - 5)
          .attr("x",60 - (this.axisHeight / 2))
          .attr("dy", "1em")
          .style("font-weight", "bold")
          .text("Temperatur (°C)")

      svg.append("text")
          .attr("transform", "translate(200,290)")
          .style("font-weight", "bold")
          .text("Zeit")

      svg.append("defs")
          .append("clipPath")
          .attr("id", "clip")
          .append("rect")
          .attr("width", this.axisWidth - 100)
          .attr("height", this.axisHeight - 250)

      // x-Achse wird aufgerufen
      let xAxisTranslate = this.axisHeight/2
      svg.append("g")
          .attr("transform", "translate(0, " + xAxisTranslate + ")")
          .call(xAxis)

      // y-Achse wird aufgerufen
      svg.append("g")
          .call(yAxis)

      let line = d3.line<graphTempData>()
          .x(function (d){return xScale(d["xDate"])})
          .y(function (d){return yScale(d["yTempSHT"])})

      // Der "path" muss vorne geclipped(abgeschnitten) werden und Werte müssen immer wieder ans Ende gepackt werden
      // attr clip-path beispiel: https://gist.github.com/mbostock/1642874
      // Möglichkeit Räume auszuwählen muss auch noch gemacht werden...

      svg.append("path")
          .data(tempSensorData)
          .attr("class", "line")
          .attr("d", line(tempSensorData))

      },

    createRHAxis(){

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