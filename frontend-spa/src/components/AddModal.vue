<template>
  <transition name="add-modal-transition">
    <div v-show="isActive" class="add-modal">
      <transition name="modal-inner-animation">
        <div v-show="isActive" class="inner-modal">
          <fa class="modal-close" @click="closeModal" icon="times-circle"></fa>
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

.modal-close {
  left: 1130px;
  top: 174px;
  z-index: 2;
}

</style>
