<template>
  <div class="sketching-board">
    <span>{{ mousePosX }}, {{ mousePosY }}</span>
    <div class="board">
      <canvas ref="drawingCanvas" :width="width" :height="height" @mousemove="getMouseCoordinatesInCanvas"
              @click="drawPoint"></canvas>
    </div>
<!--    <h1 v-for="point in tempPoints" :key="point">{{ point }}</h1>-->
  </div>
  <div class="modal-container">
    <add-modal @close="toggleModal" :is-active="modalActive">
      <div class="modal-content">
        <h1>ADD ROOM</h1>
        <p> add here name input and save button </p>
      </div>
    </add-modal>
    <button class="button is-primary" @click="toggleModal" v-show="!modalActive" type="button">ADD ROOM</button>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, ref, toRefs} from 'vue';
import Room from "@/../../models/Room";
import {Sensor} from "@/../../models/Sensor";
import Point from "@/../../models/Point";
import AddModal from '@/components/AddModal.vue'

export default defineComponent({
  name: 'SketchingBoard',

  components: {
    AddModal
  },
  data() {
    return {
      canvas: {} as CanvasRenderingContext2D,
      mousePosX: 0,
      mousePosY: 0,
      width: 0,
      height: 0,
      rooms: [] as Room[],
      tempPoints: [] as Point[],
      modalActive: ref(false)
    }
  },
  mounted() {
    const canvasFromView = this.$refs['drawingCanvas'] as HTMLCanvasElement
    this.canvas = canvasFromView.getContext('2d') as CanvasRenderingContext2D
    this.rooms.push(new Room("can", new Sensor(12)))
    this.width = window.innerWidth / 1.5
    this.height = window.innerHeight / 1.5
  },
  methods: {
    getMouseCoordinatesInCanvas(event: any) {
      let canvasFromView = this.$refs['drawingCanvas'] as HTMLCanvasElement
      let rect = canvasFromView.getBoundingClientRect()
      this.mousePosX = event.clientX - rect.left
      this.mousePosY = event.clientY - rect.top
    },
    drawPoint(event: any) {
      this.canvas.beginPath()
      this.canvas.arc(this.mousePosX, this.mousePosY, 7, 0, 2 * Math.PI)
      this.canvas.fillStyle = 'red'
      this.canvas.fill()
      this.tempPoints.push(new Point(this.mousePosX, this.mousePosY))
      if (this.tempPoints.length > 1)
        this.drawLineBetweenPoints(this.tempPoints[this.tempPoints.length - 1], this.tempPoints[this.tempPoints.length - 2])
    },
    drawLineBetweenPoints(currentPoint: Point, lastPoint: Point) {
      this.canvas.beginPath()
      this.canvas.moveTo(lastPoint.positionX, lastPoint.positionY)
      this.canvas.lineTo(currentPoint.positionX, currentPoint.positionY)
      this.canvas.lineWidth = 7
      this.canvas.strokeStyle = 'red'
      this.canvas.stroke()
    },
    toggleModal() {
      this.modalActive = !this.modalActive
    }
  }
});
</script>

<style lang="scss">

.sketching-board{

}
.modal-container{
  text-align: center;
  .modal-content{
    display: flex;
    flex-direction: column;
  }
}

.board {
  text-align: center;
}

canvas {
  border: 3px solid black;
  background-color: #c7b99f;
}
</style>
