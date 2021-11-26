<template>
  <div class="home">
    <SketchingBoard />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Sketching from '@/components/SketchingBoard.vue';
import SketchingBoard from "@/components/SketchingBoard.vue"; // @ is an alias to /src

export default defineComponent({
  name: 'Home',
  components: {
    SketchingBoard,
  }
});
</script>
