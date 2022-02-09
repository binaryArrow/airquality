<template>
  <div id="temp-div">
    <temperature-chart
        v-if="loaded"
        v-bind:chart-data1="tempData1"
        v-bind:chart-data2="tempData2"
        v-bind:chart-data3="tempData3"
        v-bind:x-axis="labels"
    />
    <button class="button is-success" v-bind:disabled="waitButton" @click="sixHours">6 stunden</button>
    <button class="button is-success" v-bind:disabled="waitButton" @click="oneDay">1 Tag</button>
    <button class="button is-success" v-bind:disabled="waitButton" @click="oneWeek">1 Woche</button>
  </div>
</template>

<script>
import {defineComponent} from 'vue';
import {Bar} from "vue3-chart-v2"
import TemperatureChart from "@/components/TemperatureChart.vue";
import {Communicator} from "@/service/communicator";
import moment from "moment";


export default defineComponent({
      name: "DashBoard",
      extends: Bar,
      components: {
        TemperatureChart
      },
      data() {
        return {
          // properties
          loaded: false,
          sensorData1: [],
          tempData1: [],
          sensorData2: [],
          tempData2: [],
          sensorData3: [],
          tempData3: [],
          waitButton: false,
          time: 10080, // get data for 7 days
          communicator: new Communicator(),
          labels: []
        }
      },
      created() {
        this.parseData(6 * 60, 0)
        this.setXaxisHours(6)
      },
      methods: {
        sixHours() {
          this.waitButton = true
          this.parseData(6 * 60, 6)
          this.setXaxisHours(6)
          setTimeout(() => {
            this.waitButton = false
          }, 2000)
        },
        oneDay() {
          this.waitButton = true
          this.parseData(24 * 60, 24)
          this.setXaxisHours(24)
          setTimeout(() => {
            this.waitButton = false
          }, 2000)
        },
        oneWeek() {
          this.waitButton = true
          this.parseData(168 * 60, 168)
          this.setXaxisHours(168)
          setTimeout(() => {
            this.waitButton = false
          }, 2000)
        },
        calculate6Hours() {
          this.tempData1 = []
          this.tempData2 = []
          this.tempData3 = []
          this.medianCalculation(3)
        },
        calculate24Hours() {
          this.loaded = false
          this.tempData1 = []
          this.tempData2 = []
          this.tempData3 = []
          this.medianCalculation(12)
          this.loaded = true
        },
        calculate1Week() {
          this.loaded = false
          this.tempData1 = []
          this.tempData2 = []
          this.tempData3 = []
          this.medianCalculation(84)
          this.loaded = true
        },
        medianCalculation(medianSize) {
          const medianCalculationSize = medianSize
          let median = 0
          for (let i = 0; i < this.sensorData1.length; i++) {
            if (i % medianCalculationSize !== 0 && i !== 0) {
              median += parseFloat(this.sensorData1[i - 1].tempSHT21) / 100
            } else if (i !== 0) {
              this.tempData1.push(median / medianCalculationSize)
              median = 0
            }
          }
          median = 0
          for (let i = 0; i < this.sensorData2.length; i++) {
            if (i % medianCalculationSize !== 0 && i !== 0) {
              median += parseFloat(this.sensorData2[i - 1].tempSHT21) / 100
            } else if (i !== 0) {
              this.tempData2.push(median / medianCalculationSize)
              median = 0
            }
          }
          median = 0
          for (let i = 0; i < this.sensorData3.length; i++) {
            if (i % medianCalculationSize !== 0 && i !== 0) {
              median += parseFloat(this.sensorData3[i - 1].tempSHT21) / 100
            } else if (i !== 0) {
              this.tempData3.push(median / medianCalculationSize)
              median = 0
            }
          }
        },
        async parseData(hours, options) {
          this.loaded = false
          this.sensorData1 = []
          await this.communicator.getSensorData(1, hours).then(data => {
            data.forEach(value => {
              this.sensorData1.push(value)
            })
          })
          this.sensorData2 = []
          await this.communicator.getSensorData(2, hours).then(data => {
            data.forEach(value => {
              this.sensorData2.push(value)
            })
          })
          this.sensorData3 = []
          await this.communicator.getSensorData(3, hours).then(data => {
            data.forEach(value => {
              this.sensorData3.push(value)
            })
          })
          switch (options) {
            case 0:
            case 6:
              this.calculate6Hours()
              break;
            case 24:
              this.calculate24Hours()
              break;
            case 168:
              this.calculate1Week()
              break;
          }
          this.loaded = true
        },
        setXaxisHours(hours) {
          this.labels = []
          switch (hours) {
            case 6: {
              const startDate = new Date(moment.now());
              startDate.setHours(startDate.getHours() - 6)
              for (let i = 0; i < 120; i++) {
                const date = moment(startDate).add(3, 'minutes').format('HH:mm');
                startDate.setMinutes(startDate.getMinutes() + 3)
                this.labels.push(date.toString());
              }
              break;
            }
            case 24: {
              let startDate = new Date(moment.now());
              startDate.setHours(startDate.getHours()-24)
              for (let i = 0; i < 120; i++) {
                const date = moment(startDate).add(12, 'minutes').format('HH:mm');
                startDate.setMinutes(startDate.getMinutes()+12)
                this.labels.push(date.toString());
              }
              break;
            }
            case 168: {
              let startDate = new Date(moment.now());
              startDate.setHours(startDate.getHours()-168)
              for (let i = 0; i < 120; i++) {
                const date = moment(startDate).add(84, 'minutes').format('dd:HH:mm');
                startDate.setMinutes(startDate.getMinutes()+84)
                this.labels.push(date.toString());
              }
              break;
            }
          }
        }
      }
    }
);

</script>

<style lang="scss">
#temp-div {
  height: 250px;
  width: 800px;
}

</style>