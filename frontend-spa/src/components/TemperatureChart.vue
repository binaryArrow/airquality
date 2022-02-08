<template>
  <canvas id="dashboard-canvas" ref="tempCanvas"></canvas>
</template>

<script lang="ts">
import {defineComponent, ref} from "vue";
import {Chart, registerables} from "chart.js";
import moment from "moment";
import {SensorData} from "@/../../backend/src/models/SensorData";
import {Communicator} from "@/service/communicator";

export default defineComponent({
  name: "TemperatureChart",
  props: {
    timeIntervall: ref(50) as any
  },
  watch:{
    timeIntervall:{
      handler: function (){
        this.assignTempdata()
      }
    }
  },
  data(){
    return {
      canvas: {} as HTMLCanvasElement,
      context: {} as CanvasRenderingContext2D,
      communicator: new Communicator,
      sensorData1: [] as number[],
      sensorData2: [] as number[],
      sensorData3: [] as number[],
    }
  },
  mounted() {
    Chart.register(...registerables)
    this.canvas = this.$refs['tempCanvas'] as HTMLCanvasElement
    this.context = this.canvas.getContext('2d') as CanvasRenderingContext2D

    const startDate = new Date(2020, 0, 1);
    const labels = [];
    for (let i = 0; i < 6; i++) {
      const date = moment(startDate).add(i, 'days').format('YYYY-MM-DD');
      labels.push(date.toString());
    }
    const chart = new Chart(this.context, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'sensor 1 Temperatur',
            data: [12, 2, 33, 44, 45, 12],
            borderWidth: 1,
            borderColor: '#419b41'
          },
          {
            label: 'sensor 2 Temperatur',
            data: [11, 20, 40, 22, 18, 25],
            borderWidth: 1,
            borderColor: '#14ccde'
          },
          {
            label: 'sensor 3 Temperatur',
            data: [8, 10, 30, 12, 38, 15],
            borderWidth: 1,
            borderColor: '#ac14de'
          }
        ]
      },
      options: {}
    });
  },
  methods:{
    assignTempdata(): void {
      this.communicator.getSensorData(1, this.timeIntervall).then(data => {
        data.forEach(value => {
          this.sensorData1.push(parseInt(value.tempSHT21)/100)
        })
      })
      this.communicator.getSensorData(2, this.timeIntervall).then(data => {
        data.forEach(value => {
          this.sensorData2.push(parseInt(value.tempSHT21)/100)
        })
      })
      this.communicator.getSensorData(3, this.timeIntervall).then(data => {
        data.forEach(value => {
          this.sensorData3.push(parseInt(value.tempSHT21)/100)
        })
      })
    }
  }
})
</script>

<style scoped>

</style>