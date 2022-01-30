<template>
  <div id="dash-board">
    <div id="line-chartTEMP">

    </div>
    <div id="line-chartRH">

    </div>
    <div id="line-chartCO2">

    </div>
    <div id="line-chartTVOC">

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
    // Erstellen von Random Daten (muss, glaube ich geändert werden..)
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


      // entweder Koordinatensystem oder Linie selber bewegen und sie ans Koordinatensystem anpassen

      let xAxisTranslate = this.axisHeight/2
      svg.append("g")
          .attr("transform", "translate(0, " + xAxisTranslate + ")")
          .call(xAxis)

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


      let xAxisTranslate = this.axisHeight/2
      svg.append("g")
          .attr("transform", "translate(0, " + xAxisTranslate + ")")
          .call(xAxis)

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
          .attr("transform", "translate(50,10)")
          .call(yAxis)


      let xAxisTranslate = this.axisHeight/2 + 10
      svg.append("g")
          .attr("transform", "translate(50, " + xAxisTranslate + ")")
          .call(xAxis)
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
          .attr("transform", "translate(50,10)")
          .call(yAxis)


      let xAxisTranslate = this.axisHeight/2 + 10
      svg.append("g")
          .attr("transform", "translate(50, " + xAxisTranslate + ")")
          .call(xAxis)
    },
    }

  }
);

</script>

<style lang="scss">
#dash-board{

}

#line-chartTEMP{
  width: 500px;
  height: 500px;
}

#line-chartRH{
  width: 500px;
  height: 500px;
}

#line-chartCO2{
  width: 500px;
  height: 500px;
}

#line-chartTVOC{
  width: 500px;
  height: 500px;
}

</style>