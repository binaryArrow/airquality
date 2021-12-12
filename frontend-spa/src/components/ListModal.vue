<template>
  <transition name="list-modal-transition">
    <div v-show="isActive" class="list-modal">
      <transition name="modal-inner-animation">
        <div v-show="isActive" class="inner-modal">
          <!-- modal content -->
          <table class="table">
            <tr>
              <th>Name</th>
              <th>Sensor</th>
            </tr>
            <tr v-for="(room, index) in rooms" :key="index">
              <td>
                {{room.roomName}}
              </td>
              <td>
                {{room.sensor.sensorId}}
              </td>
              <button class="button is-danger is-small is-rounded" @click="deleteRoom(index)">
              <span class="icon is-large">
                <fa icon="trash"></fa>
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
  emits: ['deleteRoom'],
  methods: {
    //TODO: mit event arbeteiten der auf parent rooms löscht
    deleteRoom(index: number) {
      this.$emit('deleteRoom', index)
    }
  }
})
</script>

<style scoped>

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

</style>