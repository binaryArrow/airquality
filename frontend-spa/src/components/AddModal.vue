<template>
  <transition name="add-modal-transition">
    <div v-show="isActive" class="add-modal">
      <transition name="modal-inner-animation">
        <div v-show="isActive" class="inner-modal">
          <fa @click="closeModal" icon="times-circle"></fa>
          <!-- modal content -->
          <slot />
<!--          <button class="button" @click="closeModal" type="button">Close</button>-->
        </div>
      </transition>
    </div>
  </transition>
</template>

<script>
export default {
  name: "AddModal",
  props:{
    isActive: Boolean
  },
  emits:['close'],
  methods: {
    closeModal(){
      this.$emit('close')
    }
  }
}
</script>

<style scoped>

</style>
