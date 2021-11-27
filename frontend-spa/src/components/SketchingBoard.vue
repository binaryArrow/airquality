<template>
  <span>{{mousePosX}}, {{mousePosY}}</span>
  <div class="board">
    <canvas ref="drawingCanvas" :width="width" :height="height" @mousemove="getMouseCoordinates"></canvas>
  </div>
  <h1 v-for="room in rooms" :key="room">{{room}}</h1>

</template>

<script lang="ts">
import {defineComponent, onMounted, ref} from 'vue';
import Room from "../../../models/Room";
import {Sensor} from "../../../models/Sensor";

export default defineComponent({
  name: 'SketchingBoard',

  data(){
    return{
      canvas: {} as CanvasRenderingContext2D,
      mousePosX: 0,
      mousePosY: 0,
      width: 0,
      height:0,
      rooms: [] as Room[]
    }
  },
  mounted() {
    let canvasFromView = this.$refs['drawingCanvas'] as HTMLCanvasElement
    this.canvas = canvasFromView.getContext('2d') as CanvasRenderingContext2D
    this.rooms.push(new Room("can", new Sensor(12)))
    this.width = window.innerWidth / 1.5
    this.height = window.innerHeight/1.5
  },
  methods:{
    getMouseCoordinates(event: any){
      this.mousePosX = event.pageX
      this.mousePosY = event.pageY
    }
  }
});
</script>

<style lang="scss">

.board{
  text-align: center;
}

canvas{
  border: 3px solid black;
}
</style>
