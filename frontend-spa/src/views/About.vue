<template>
  <div class="about">
    <h1></h1>
    <DashBoard />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import DashBoard from "@/components/DashBoard.vue";

export default defineComponent({
  name: 'About',
  components: {
        DashBoard,
  }
});
</script>
