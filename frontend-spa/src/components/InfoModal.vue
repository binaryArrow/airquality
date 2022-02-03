<template>
  <transition name="info-modal-transition">
    <div v-show="isActive" class="add-modal">
      <transition name="modal-inner-animation">
        <div v-show="isActive" class="inner-modal">
          <!-- modal content -->
          <table class="table">
            <tr>
              <th>Sensor</th>
              <th>Data</th>
            </tr>
            <tr>Temp-SHT21:<td>{{sensorData.tempSHT21/100 + " °C"}} </td> </tr>
            <tr>Hum-SHT21: <td>{{sensorData.humSHT21/100 + " %RH"}}</td></tr>
            <tr>Temp-SCD41: <td>{{sensorData.tempSCD41/100 + " °C"}}</td> </tr>
            <tr>Hum-SCD41: <td>{{sensorData.humSCD41/100 + " %RH"}}</td> </tr>
            <tr>CO2-SCD41: <td>{{sensorData.co2SCD41 + " ppm"}}</td></tr>
            <tr>ECO2-CCS811: <td>{{sensorData.eco2CCS811 + " ppm"}}</td></tr>
            <tr>TVOC-CCS811: <td>{{sensorData.tvocCCS811 + " ppb"}}</td></tr>
          </table>
          <slot />
          <!--          <button class="button" @click="closeModal" type="button">Close</button>-->
        </div>
      </transition>
    </div>
  </transition>
</template>
y
<script>
import {SensorData} from "@/../../backend/src/models/SensorData"
export default {
  name: "InfoModal",
  props:{
    isActive: Boolean,
    sensorData: SensorData
  }
}
</script>

<style scoped>
.add-modal-transition-enter-active,
.add-modal-transition-leave-active{
  transition: opacity .3s ease-in;
}

.add-modal-transition-enter-from,
.add-modal-transition-leave-to {
  opacity: 0;
}

.modal-inner-animation-enter-active,
.modal-inner-animation-leave-active {
  transition: all .3s ease-in 0.15s;
}

.modal-inner-animation-enter-from,
.modal-inner-animation-leave-to {
  opacity: 0;
}

.inner-modal {
  height: 300px;
  overflow: auto;
}

th {
  position: sticky;
  top: 0;
  z-index: 1;
  background: #ffffff;
}

#close-button {
  position: absolute;
  right: 20px;
  top: 3px;
}

</style>
