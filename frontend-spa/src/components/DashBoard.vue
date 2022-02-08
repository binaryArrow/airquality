<template>
  <div id="temp-div">
    <temperature-chart :time-intervall="this.time"></temperature-chart>
  </div>
  <button @click="changeTime">time-intervall</button>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {SensorData} from "@/../../backend/src/models/SensorData";
import {io} from "socket.io-client";
import TemperatureChart from "@/components/TemperatureChart.vue";
import {Communicator} from "@/service/communicator";

const socket = io("http://localhost:3000")

export default defineComponent({
      name: "DashBoard",
      components: {
        TemperatureChart
      },
      data() {
        return {
          time: 50
        }
      },
      methods: {
        changeTime() {
          this.time = Math.floor(Math.random() * (100 - 50) + 50)
        }
      }
    }
);

</script>

<style lang="scss">
#temp-div {
  height: 250px;
  width: 500px;
}

</style>