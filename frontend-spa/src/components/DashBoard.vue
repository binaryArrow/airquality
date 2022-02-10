<template>
  <div id="temp-div">
    <temperature-chart
        v-if="loaded"
        v-bind:chart-data1="tempData1"
        v-bind:chart-data2="tempData2"
        v-bind:chart-data3="tempData3"
        v-bind:x-axis="labelsTemp"
    />
    <button class="button is-success" v-bind:disabled="waitButton" @click="sixHours('temperature')">6 Stunden</button>
    <button class="button is-success" v-bind:disabled="waitButton" @click="oneDay('temperature')">1 Tag</button>
    <button class="button is-success" v-bind:disabled="waitButton" @click="oneWeek('temperature')">1 Woche</button>
  </div>
  <div id="hum-div">
    <humidity-chart
        v-if="loaded"
        v-bind:chart-data1="humData1"
        v-bind:chart-data2="humData2"
        v-bind:chart-data3="humData3"
        v-bind:x-axis="labelsHum"
    />
    <button class="button is-success" v-bind:disabled="waitButton" @click="sixHours('humidity')">6 Stunden</button>
    <button class="button is-success" v-bind:disabled="waitButton" @click="oneDay('humidity')">1 Tag</button>
    <button class="button is-success" v-bind:disabled="waitButton" @click="oneWeek('humidity')">1 Woche</button>
  </div>
  <div id="co2-div">
    <co2-chart
        v-if="loaded"
        v-bind:chart-data1="co2Data1"
        v-bind:chart-data2="co2Data2"
        v-bind:chart-data3="co2Data3"
        v-bind:x-axis="labelsCo2"
    />
    <button class="button is-success" v-bind:disabled="waitButton" @click="sixHours('co2')">6 Stunden</button>
    <button class="button is-success" v-bind:disabled="waitButton" @click="oneDay('co2')">1 Tag</button>
    <button class="button is-success" v-bind:disabled="waitButton" @click="oneWeek('co2')">1 Woche</button>
  </div>
</template>

<script>
import {defineComponent} from 'vue';
import {Bar} from "vue3-chart-v2";
import TemperatureChart from "@/components/TemperatureChart.vue";
import Co2Chart from "@/components/Co2Chart.vue";
import HumidityChart from "@/components/HumidityChart";
import {Communicator} from "@/service/communicator";
import moment from "moment";


export default defineComponent({
      name: "DashBoard",
      extends: Bar,
      components: {
        TemperatureChart,
        HumidityChart,
        Co2Chart
      },
      data() {
        return {
          // properties
          loaded: false,
          sensorData1: [],
          tempData1: [],
          humData1: [],
          co2Data1: [],
          sensorData2: [],
          tempData2: [],
          humData2: [],
          co2Data2: [],
          sensorData3: [],
          tempData3: [],
          humData3: [],
          co2Data3: [],
          waitButton: false,
          communicator: new Communicator(),
          labelsTemp: [],
          labelsHum: [],
          labelsCo2: []
        }
      },
      created() {
        this.parseData(6 * 60, 0)
        this.setXaxisHours(6, "temperature")
        this.setXaxisHours(6, "co2")
        this.setXaxisHours(6, "humidity")
      },
      methods: {
        sixHours(options) {
          this.waitButton = true
          if (options === "temperature") {
            this.parseData(6 * 60, 6, options)
            this.setXaxisHours(6, options)
          } else if (options === "humidity") {
            this.parseData(6 * 60, 6, options)
            this.setXaxisHours(6, options)
          } else if (options === "co2") {
            this.parseData(6 * 60, 6, options)
            this.setXaxisHours(6, options)
          }
          setTimeout(() => {
            this.waitButton = false
          }, 2000)
        },
        oneDay(options) {
          this.waitButton = true
          if (options === "temperature") {
            this.parseData(24 * 60, 24, options)
            this.setXaxisHours(24, options)
          } else if (options === "humidity") {
            this.parseData(24 * 60, 24, options)
            this.setXaxisHours(24, options)
          } else if (options === "co2") {
            this.parseData(24 * 60, 6, options)
            this.setXaxisHours(24, options)
          }
          setTimeout(() => {
            this.waitButton = false
          }, 2000)
        },
        oneWeek(options) {
          this.waitButton = true
          if (options === "temperature") {
            this.parseData(168 * 60, 168, options)
            this.setXaxisHours(168, options)
          } else if (options === "humidity") {
            this.parseData(168 * 60, 168, options)
            this.setXaxisHours(168, options)
          } else if (options === "co2") {
            this.parseData(168 * 60, 6, options)
            this.setXaxisHours(168, options)
          }
          setTimeout(() => {
            this.waitButton = false
          }, 2000)
        },
        calculate6Hours(options) {
          if (options === "temperature") {
            this.tempData1 = []
            this.tempData2 = []
            this.tempData3 = []
            this.medianCalculation(3, options)
          } else if (options === "humidity") {
            this.humData1 = []
            this.humData2 = []
            this.humData3 = []
            this.medianCalculation(3, options)
          } else if (options === "co2") {
            this.co2Data1 = []
            this.co2Data2 = []
            this.co2Data3 = []
            this.medianCalculation(3, options)
          }
        },
        calculate24Hours(options) {
          this.loaded = false
          if (options === "temperature") {
            this.tempData1 = []
            this.tempData2 = []
            this.tempData3 = []
            this.medianCalculation(12, options)
          } else if (options === "humidity") {
            this.humData1 = []
            this.humData2 = []
            this.humData3 = []
            this.medianCalculation(12, options)
          } else if (options === "co2") {
            this.co2Data1 = []
            this.co2Data2 = []
            this.co2Data3 = []
            this.medianCalculation(12, options)
          }
          this.loaded = true
        },
        calculate1Week(options) {
          this.loaded = false
          if (options === "temperature") {
            this.tempData1 = []
            this.tempData2 = []
            this.tempData3 = []
            this.medianCalculation(84, options)
          } else if (options === "humidity") {
            this.humData1 = []
            this.humData2 = []
            this.humData3 = []
            this.medianCalculation(84, options)
            this.loaded = true
          } else if (options === "co2") {
            this.co2Data1 = []
            this.co2Data2 = []
            this.co2Data3 = []
            this.medianCalculation(84, options)
          }
        },
        medianCalculation(medianSize, options) {
          const medianCalculationSize = medianSize
          if (options === "temperature") {
            let finalSensorData1 = []
            let variableForData = 0
            for (let i = 0; i < 120; i++) {
              this.tempData1.push(0)
            }
            for (let i = 0; i < this.sensorData1.length; i++) {
              if (i % medianCalculationSize === 0 && i !== 0) {
                if (this.sensorData1[i])
                  finalSensorData1.push(parseFloat(this.sensorData1[i].tempSHT21) / 100)
                console.log(finalSensorData1)
              }
            }
            for (let i = 119; i >= 0; i--) {
              if (variableForData < finalSensorData1.length) {
                this.tempData1[i] = finalSensorData1[variableForData]
              }
              variableForData++
            }
            for (let i = 0; i < this.sensorData2.length; i++) {
              if (i % medianCalculationSize !== 0 && i !== 0) {
                this.tempData2.push(parseFloat(this.sensorData2[i - 1].tempSHT21) / 100)
              }
            }
            for (let i = 0; i < this.sensorData3.length; i++) {
              if (i % medianCalculationSize !== 0 && i !== 0) {
                this.tempData3.push(parseFloat(this.sensorData3[i - 1].tempSHT21) / 100)
              }
            }
          }
          // else if (options === "co2") {
          //   median = 0
          //   for (let i = 0; i < this.sensorData1.length; i++) {
          //     if (i % medianCalculationSize !== 0 && i !== 0) {
          //       median += parseFloat(this.sensorData1[i - 1].co2SCD41) / 100
          //     } else if (i !== 0) {
          //       this.co2Data1.push(median / medianCalculationSize)
          //       median = 0
          //     }
          //   }
          //   median = 0
          //   for (let i = 0; i < this.sensorData2.length; i++) {
          //     if (i % medianCalculationSize !== 0 && i !== 0) {
          //       median += parseFloat(this.sensorData2[i - 1].co2SCD41) / 100
          //     } else if (i !== 0) {
          //       this.co2Data2.push(median / medianCalculationSize)
          //       median = 0
          //     }
          //   }
          //   median = 0
          //   for (let i = 0; i < this.sensorData3.length; i++) {
          //     if (i % medianCalculationSize !== 0 && i !== 0) {
          //       median += parseFloat(this.sensorData3[i - 1].co2SCD41) / 100
          //     } else if (i !== 0) {
          //       this.co2Data3.push(median / medianCalculationSize)
          //       median = 0
          //     }
          //   }
          // } else if (options === "humidity") {
          //   for (let i = 0; i < this.sensorData1.length; i++) {
          //     if (i % medianCalculationSize !== 0 && i !== 0) {
          //       median += parseFloat(this.sensorData1[i - 1].humSHT21) / 100
          //     } else if (i !== 0) {
          //       this.humData1.push(median / medianCalculationSize)
          //       median = 0
          //     }
          //   }
          //   median = 0
          //   for (let i = 0; i < this.sensorData2.length; i++) {
          //     if (i % medianCalculationSize !== 0 && i !== 0) {
          //       median += parseFloat(this.sensorData2[i - 1].humSHT21) / 100
          //     } else if (i !== 0) {
          //       this.humData2.push(median / medianCalculationSize)
          //       median = 0
          //     }
          //   }
          //   median = 0
          //   for (let i = 0; i < this.sensorData3.length; i++) {
          //     if (i % medianCalculationSize !== 0 && i !== 0) {
          //       median += parseFloat(this.sensorData3[i - 1].humSHT21) / 100
          //     } else if (i !== 0) {
          //       this.humData3.push(median / medianCalculationSize)
          //       median = 0
          //     }
          //   }
          // }
        },
        async parseData(dataSet, options, optionsDecide) {
          this.loaded = false
          this.sensorData1 = []
          await this.communicator.getSensorData(1, dataSet, options).then(data => {
            data.forEach(value => {
              this.sensorData1.push(value)
            })
          })
          this.sensorData2 = []
          await this.communicator.getSensorData(2, dataSet, options).then(data => {
            data.forEach(value => {
              this.sensorData2.push(value)
            })
          })
          this.sensorData3 = []
          await this.communicator.getSensorData(3, dataSet, options).then(data => {
            data.forEach(value => {
              this.sensorData3.push(value)
            })
          })
          switch (options) {
            case 0: {
              this.calculate6Hours("temperature")
              this.calculate6Hours("co2")
              this.calculate6Hours("humidity")
              break
            }
            case 6:
              this.calculate6Hours(optionsDecide)
              break;
            case 24:
              this.calculate24Hours(optionsDecide)
              break;
            case 168:
              this.calculate1Week(optionsDecide)
              break;
          }
          this.loaded = true
        },
        setXaxisHours(hours, options) {
          if (options === "temperature") {
            this.labelsTemp = []
            switch (hours) {
              case 6: {
                const startDate = new Date(moment.now());
                startDate.setHours(startDate.getHours() - 6)
                for (let i = 0; i < 120; i++) {
                  const date = moment(startDate).add(3, 'minutes').format('HH:mm');
                  startDate.setMinutes(startDate.getMinutes() + 3)
                  this.labelsTemp.push(date.toString());
                }
                break;
              }
              case 24: {
                let startDate = new Date(moment.now());
                startDate.setHours(startDate.getHours() - 24)
                for (let i = 0; i < 120; i++) {
                  const date = moment(startDate).add(12, 'minutes').format('HH:mm');
                  startDate.setMinutes(startDate.getMinutes() + 12)
                  this.labelsTemp.push(date.toString());
                }
                break;
              }
              case 168: {
                let startDate = new Date(moment.now());
                startDate.setHours(startDate.getHours() - 168)
                for (let i = 0; i < 120; i++) {
                  const date = moment(startDate).add(84, 'minutes').format('dd:HH:mm');
                  startDate.setMinutes(startDate.getMinutes() + 84)
                  this.labelsTemp.push(date.toString());
                }
                break;
              }
            }
          } else if (options === "co2") {
            this.labelsCo2 = []
            switch (hours) {
              case 6: {
                const startDate = new Date(moment.now());
                startDate.setHours(startDate.getHours() - 6)
                for (let i = 0; i < 120; i++) {
                  const date = moment(startDate).add(3, 'minutes').format('HH:mm');
                  startDate.setMinutes(startDate.getMinutes() + 3)
                  this.labelsCo2.push(date.toString());
                }
                break;
              }
              case 24: {
                let startDate = new Date(moment.now());
                startDate.setHours(startDate.getHours() - 24)
                for (let i = 0; i < 120; i++) {
                  const date = moment(startDate).add(12, 'minutes').format('HH:mm');
                  startDate.setMinutes(startDate.getMinutes() + 12)
                  this.labelsCo2.push(date.toString());
                }
                break;
              }
              case 168: {
                let startDate = new Date(moment.now());
                startDate.setHours(startDate.getHours() - 168)
                for (let i = 0; i < 120; i++) {
                  const date = moment(startDate).add(84, 'minutes').format('dd:HH:mm');
                  startDate.setMinutes(startDate.getMinutes() + 84)
                  this.labelsCo2.push(date.toString());
                }
                break;
              }
            }
          } else if (options === "humidity") {
            this.labelsHum = []
            switch (hours) {
              case 6: {
                const startDate = new Date(moment.now());
                startDate.setHours(startDate.getHours() - 6)
                for (let i = 0; i < 120; i++) {
                  const date = moment(startDate).add(3, 'minutes').format('HH:mm');
                  startDate.setMinutes(startDate.getMinutes() + 3)
                  this.labelsHum.push(date.toString());
                }
                break;
              }
              case 24: {
                let startDate = new Date(moment.now());
                startDate.setHours(startDate.getHours() - 24)
                for (let i = 0; i < 120; i++) {
                  const date = moment(startDate).add(12, 'minutes').format('HH:mm');
                  startDate.setMinutes(startDate.getMinutes() + 12)
                  this.labelsHum.push(date.toString());
                }
                break;
              }
              case 168: {
                let startDate = new Date(moment.now());
                startDate.setHours(startDate.getHours() - 168)
                for (let i = 0; i < 120; i++) {
                  const date = moment(startDate).add(84, 'minutes').format('dd:HH:mm');
                  startDate.setMinutes(startDate.getMinutes() + 84)
                  this.labelsHum.push(date.toString());
                }
                break;
              }
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

#hum-div {
  height: 250px;
  width: 800px;
  position: relative;
  left: 850px;
  bottom: 250px;
}

#co2-div {
  height: 250px;
  width: 800px;
  position: relative;
}

</style>