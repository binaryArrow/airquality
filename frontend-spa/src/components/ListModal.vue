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
                <select class="select" v-model="room.sensor">
                  <option v-bind:value="{sensorId: 0}">0</option>
                  <option v-bind:value="{sensorId: 1}">1</option>
                  <option v-bind:value="{sensorId: 2}">2</option>
                  <option v-bind:value="{sensorId: 3}">3</option>
                </select>
              </td>
              <button class="button is-danger is-small is-rounded" @click="deleteRoom(index)">
              <span class="icon is-large">
                <fa icon="trash"></fa>
              </span>
              </button>
              <button class="button is-warning is-small is-rounded" @click="showInfo(index)">
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
  emits: ['deleteRoom', 'showInfo', 'close'],
  methods: {
    deleteRoom(index: number) {
      this.$emit('deleteRoom', index)
    },
    showInfo(index: number) {
      this.$emit('showInfo', index)
    },
    closeModal() {
      this.$emit('close', 'list')
    }
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
th{
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