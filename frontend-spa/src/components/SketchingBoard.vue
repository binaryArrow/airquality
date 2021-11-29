<template>
  <span>{{ mousePosX }}, {{ mousePosY }}</span>
  <div class="sketching-board">
    <div class="board">
      <canvas ref="drawingCanvas" :width="width" :height="height" @mousemove="getMouseCoordinatesInCanvas"
              @click="drawPoint"></canvas>
    </div>
    <div class="modal-container">
      <add-modal @close="toggleModal" :is-active="modalActive">
        <div class="modal-content">
          <p><b>{{ addInformation }}</b></p>
          <input v-bind:class="addInputClassName" type="text" v-model="newRoomName" placeholder="Rooom name">
          <button class="button is-success" @click="addNewRoom">ADD</button>
        </div>
      </add-modal>
    </div>
    <div class="add-button-wrapper">
      <button id="add-button" class="button is-primary" @click="toggleModal" v-show="!modalActive" type="button">ADD
        ROOM
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent, ref} from 'vue';
import Room from "@/../../models/Room";
import Sensor from "@/../../models/Sensor";
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
      canvasFromView: {} as HTMLCanvasElement,
      mousePosX: 0,
      mousePosY: 0,
      width: 0,
      height: 0,
      rooms: [] as Room[],
      tempPoints: [] as Point[],
      modalActive: ref(false),
      newRoomName: '',
      addInformation: 'add a name for the room',
      addInputClassName: 'input is-rounded'
    }
  },
  mounted() {
    this.canvasFromView = this.$refs['drawingCanvas'] as HTMLCanvasElement
    this.canvas = this.canvasFromView.getContext('2d') as CanvasRenderingContext2D
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
    drawPoint() {
      this.canvas.beginPath()
      this.canvas.arc(this.mousePosX, this.mousePosY, 7, 0, 2 * Math.PI)
      this.canvas.fillStyle = 'red'
      this.canvas.fill()
      this.tempPoints.push(new Point(this.mousePosX, this.mousePosY))
      if (this.tempPoints.length > 1)
        this.drawLineBetweenPoints(this.tempPoints[this.tempPoints.length - 1], this.tempPoints[this.tempPoints.length - 2])
    },
    drawExistingPoint(point: Point) {
      this.canvas.beginPath()
      this.canvas.arc(
          point.positionX,
          point.positionY,
          7,
          0,
          2 * Math.PI
      )
      this.canvas.fillStyle = 'green'
      this.canvas.fill()
    },
    drawLineBetweenPoints(currentPoint: Point, lastPoint: Point, points?: Point[]) {
      if (!points) {
        this.canvas.beginPath()
        this.canvas.moveTo(lastPoint.positionX, lastPoint.positionY)
        this.canvas.lineTo(currentPoint.positionX, currentPoint.positionY)
        this.canvas.lineWidth = 7
        this.canvas.strokeStyle = 'red'
        this.canvas.stroke()
      } else {
        for (let i = 1; i < points?.length; i++) {
          this.canvas.beginPath()
          this.canvas.moveTo(points[i - 1].positionX, points[i - 1].positionY)
          this.canvas.lineTo(points[i].positionX, points[i].positionY)
          this.canvas.lineWidth = 7
          this.canvas.strokeStyle = 'green'
          this.canvas.stroke()
        }
      }
    },
    toggleModal() {
      this.addInputClassName = 'input is-rounded'
      if (this.tempPoints.length > 1)
        this.modalActive = !this.modalActive
    },
    addNewRoom() {
      if (this.newRoomName.length < 1) {
        this.addInformation = 'Enter a Room name first!!!'
        this.addInputClassName = 'input is-rounded is-danger'
      } else {
        let newRoom = new Room(this.newRoomName, this.tempPoints)
        this.rooms.push(newRoom)
        this.newRoomName = ''
        this.tempPoints = []
        this.modalActive = false
        this.redrawCavas(this.rooms)
      }
    },
    redrawCavas(existingRooms: Room[]) {
      this.canvas.clearRect(0, 0, this.canvasFromView.width, this.canvasFromView.height)
      existingRooms.forEach((room) => {
        room.points.forEach((point) => {
          this.drawExistingPoint(point)
        })
        this.drawLineBetweenPoints(new Point(0, 0), new Point(0, 0), room.points)
      })
    }
  }
});
</script>

<style lang="scss">

.sketching-board {
  display: grid;
  text-align: center;
}

.modal-container {
  grid-column: 1;
  grid-row: 1;

  .modal-content {
    top: 40px;
    background: #ffffff;
    width: 400px;
    border-radius: 10px;
  }
}

.board {
  grid-column: 1;
  grid-row: 1;
}

.add-button-wrapper {
  display: flex;
  flex-direction: row;
  justify-content: center;
  #add-button {
    width: 100px;
    height: 35px;
  }
}

canvas {
  border: 3px solid black;
  background-color: #c7b99f;
}
</style>
