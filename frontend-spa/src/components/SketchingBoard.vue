<template>
  <span>{{mousePosX}}, {{mousePosY}}</span>
  <div class="board">
    <canvas ref="drawingCanvas" :width="width" :height="height" @mousemove="getMouseCoordinatesInCanvas" @click="drawPoint"></canvas>
  </div>
  <h1 v-for="point in tempPoints" :key="point">{{point}}</h1>

</template>

<script lang="ts">
import {defineComponent, onMounted, ref} from 'vue';
import Room from "../../../models/Room";
import {Sensor} from "../../../models/Sensor";
import Point from "../../../models/Point";

export default defineComponent({
  name: 'SketchingBoard',

  data(){
    return{
      canvas: {} as CanvasRenderingContext2D,
      mousePosX: 0,
      mousePosY: 0,
      width: 0,
      height:0,
      rooms: [] as Room[],
      tempPoints: [] as Point[]
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
    getMouseCoordinatesInCanvas(event: any){
      let canvasFromView = this.$refs['drawingCanvas'] as HTMLCanvasElement
      let rect = canvasFromView.getBoundingClientRect()
      this.mousePosX = event.clientX - rect.left
      this.mousePosY = event.clientY - rect.top
    },
    drawPoint(event: any){
      this.canvas.beginPath()
      this.canvas.arc(this.mousePosX, this.mousePosY, 10, 0, 2 * Math.PI)
      this.canvas.fillStyle = 'black'
      this.canvas.fill()
      this.tempPoints.push(new Point(this.mousePosX, this.mousePosY))
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
