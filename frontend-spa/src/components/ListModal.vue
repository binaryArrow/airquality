<template>
  <transition name="list-modal-transition">
    <div v-show="isActive" class="list-modal">
      <transition name="modal-inner-animation">
        <div v-show="isActive" class="inner-modal">
          <!-- modal content -->
          <table class="table">
            <fa id="close-button" icon="times-circle" @click="closeModal"></fa>
            <tr>
              <th>Name</th>
              <th>Sensor</th>
              <th></th>
            </tr>
            <tr v-for="(room, index) in rooms" :key="index">
              <td>
                {{ room.roomName }}
              </td>
              <td>
                <select class="select" v-model="room.sensorId" @input="lookForDoubleEntries(room.sensorId, room.id, $event)">
                  <option v-bind:value="0">0</option>
                  <option v-bind:disabled="disabled1" v-bind:value="1">1</option>
                  <option v-bind:disabled="disabled2" v-bind:value="2">2</option>
                  <option v-bind:disabled="disabled3" v-bind:value="3">3</option>
                </select>
              </td>
              <button class="button is-danger is-small is-rounded" @click="deleteRoom(room.sensorId, index)">
              <span class="icon is-large">
                <fa icon="trash"></fa>
              </span>
              </button>
              <button class="button is-warning is-small is-rounded" @click="showInfo(room.sensorId)">
              <span class="icon is-large">
                <fa icon="info"></fa>
              </span>
              </button>
            </tr>
          </table>
          <slot/>
          <!--          <button class="button" @click="closeModal" type="button">Close</button>-->
        </div>
      </transition>
    </div>
  </transition>
</template>

<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  name: "ListModal",
  props: {
    rooms: Array,
    isActive: Boolean
  },
  data() {
    return {
      disabled1: false,
      disabled2: false,
      disabled3: false,
      ampel: "ampel"
    }
  },
  emits: ['deleteRoom', 'showInfo', 'close', 'sensorAdded', 'closeInfoModal'],

  methods: {
    lookForDoubleEntries(sensorId: number, roomId: number, e: any){
      // new value for sensorID
      switch (e.target.value){
        case "1": {
          this.disabled1 = true
          break
        }
        case "2": {
          this.disabled2 = true
          break
        }
        case "3": {
          this.disabled3 = true
          break
        }
      }
      // old value of sensor Id
      switch (sensorId){
        case 1: {
          this.disabled1 = false
          break
        }
        case 2: {
          this.disabled2 = false
          break
        }
        case 3: {
          this.disabled3 = false
          break
        }
      }
      this.$emit('sensorAdded', roomId, e.target.value, sensorId)
      this.$emit('closeInfoModal')
    },
    deleteRoom(sensorId: number, index: number) {
      console.log(sensorId)
      switch (sensorId){
        case 1: {
          this.disabled1 = false
          break
        }
        case 2: {
          this.disabled2 = false
          break
        }
        case 3: {
          this.disabled3 = false
          break
        }
      }
      this.$emit('deleteRoom', index, sensorId)
    },
    showInfo(sensorId: number) {
      this.$emit('showInfo', sensorId)
    },
    closeModal() {
      this.$emit('close', 'list')
    },
  }
})
</script>

<style scoped lang="scss">

.list-modal-transition-enter-active,
.list-modal-transition-leave-active {
  transition: opacity .3s ease-in;
}

.list-modal-transition-enter-from,
.list-modal-transition-leave-to {
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
  height: 200px;
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