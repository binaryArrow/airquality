<template>
  <div class="sketching-board">
    <div class="board">
      <canvas ref="drawingCanvas" :width="width" :height="height"></canvas>
    </div>
    <div class="modal-container">
      <add-modal :is-active="modalActive">
        <div class="modal-content">
          <p><b>{{ addInformation }}</b></p>
          <input v-bind:class="addInputClassName" type="text" v-model="newRoomName" placeholder="Rooom name">
          <button class="button is-success" @click="addNewRoom">ADD</button>
          <button class="button is-danger" @click="toggleModal">CANCEL</button>
        </div>
      </add-modal>
    </div>
  </div>
  <div class="add-button-wrapper">
    <button id="add-button" class="button is-primary" @click="toggleModal" v-show="!modalActive" type="button">ADD
      ROOM
    </button>
  </div>
</template>

<script lang="ts">
import {defineComponent, ref} from 'vue';
import Room from "@/../../models/Room";
import Sensor from "@/../../models/Sensor";
import Point from "@/../../models/Point";
import AddModal from '@/components/AddModal.vue'
import {fabric} from "fabric";
import {Circle, Line, Object} from "fabric/fabric-impl";

interface CircleWithLine extends fabric.Object, fabric.Circle {
  line1?: fabric.Line,
  line2?: fabric.Line
}

export default defineComponent({
  name: 'SketchingBoard',

  components: {
    AddModal
  },
  data() {
    return {
      canvas: {} as fabric.Canvas,
      canvasFromView: {} as HTMLCanvasElement,
      mousePosX: 0,
      mousePosY: 0,
      height: 800,
      width: 1200,
      grid: 20,
      rooms: [] as Room[],
      modalActive: ref(false),
      newRoomName: '',
      addInformation: 'add a name for the room',
      addInputClassName: 'input is-rounded'
    }
  },
  mounted() {
    this.canvasFromView = this.$refs['drawingCanvas'] as HTMLCanvasElement
    this.canvas = new fabric.Canvas(this.canvasFromView)
    this.drawGrid()
    this.canvas.on('selection:created', (event)=> {
      if (event.target)
      event.target.set({
        lockScalingY: true,
        lockScalingX: true
      })
    })
    this.canvas.on("mouse:dblclick", (options)=>{
      this.mousePosX = options.e.clientX - this.canvasFromView.getBoundingClientRect().left
      this.mousePosY = options.e.clientY - this.canvasFromView.getBoundingClientRect().top
      this.addPoint()
    })
    this.canvas.on('object:moving', (options) => {
      if (options.target) {
        let target = options.target as CircleWithLine
        if (target.left && target.top) {
          target.left = Math.round(target.left / this.grid) * this.grid
          target.top = Math.round(target.top / this.grid) * this.grid
          if (target.line1)
            target.line1 && target.line1.set({x2: target.left, y2: target.top})
          if (target.line2)
            target.line2 && target.line2.set({x1: target.left, y1: target.top})
        }
      }
    })

  },
  methods: {
    drawGrid(){
      for (let i = 0; i < (this.width / this.grid); i++) {
        this.canvas.add(new fabric.Line([i * this.grid, 0, i * this.grid, this.height], {
          stroke: '#ccc',
          selectable: false,
          hoverCursor: 'false'
        }));
        this.canvas.add(new fabric.Line([0, i * this.grid, this.width, i * this.grid], {
          stroke: '#ccc',
          selectable: false,
          hoverCursor: 'false'
        }))
      }
    },
    addPoint() {
      let newPoint = this.makeCircle(this.mousePosX, this.mousePosY)
      let newLine
      this.canvas.add(newPoint)
      if (this.canvas.getObjects('circle').length >= 2) {
        newLine = this.makeLine([
          this.canvas.getObjects('circle')[this.canvas.getObjects('circle').length - 2].getCenterPoint().x,
          this.canvas.getObjects('circle')[this.canvas.getObjects('circle').length - 2].getCenterPoint().y,
          this.canvas.getObjects('circle')[this.canvas.getObjects('circle').length - 1].getCenterPoint().x,
          this.canvas.getObjects('circle')[this.canvas.getObjects('circle').length - 1].getCenterPoint().y,
        ])
        if (newLine)
          this.canvas.add(newLine)
      }
      if (this.canvas.getObjects('line').length >= 121) {
        let firstLine = this.canvas.getObjects('circle')[this.canvas.getObjects('circle').length - 1] as CircleWithLine
        firstLine.set("line1", newLine)
        let secondLine = this.canvas.getObjects('circle')[this.canvas.getObjects('circle').length - 2] as CircleWithLine
        secondLine.set("line2", newLine)
      }
      console.log(this.canvas.getObjects('circle'))
    },
    makeLine(coords: number[]) {
      return new fabric.Line(coords, {
        stroke: 'red',
        strokeWidth: 3,
        lockScalingX: true,
        lockScalingY: true
      })
    },
    makeCircle(left: number, top: number, line1?: fabric.Line, line2?: fabric.Line): Circle {
      const opt = {
        left: Math.round(left / this.grid) * this.grid,
        top: Math.round(top / this.grid) * this.grid,
        radius: 5,
        fill: 'red',
        originX: 'center',
        originY: 'center',
        centeredRotation: true,
        strokeWidth: 2,
        lockRotation: true,
        lockScalingX: true,
        lockScalingY: true,
        line1: line1,
        line2: line2,
        hasControls: false,
        hasBorders: false
      } as CircleWithLine

      return new fabric.Circle(opt)

    },
    // drawExistingPoint(point: Point) {
    //   this.canvas.beginPath()
    //   this.canvas.arc(
    //       point.positionX,
    //       point.positionY,
    //       7,
    //       0,
    //       2 * Math.PI
    //   )
    //   this.canvas.fillStyle = 'green'
    //   this.canvas.fill()
    // },
    toggleModal() {
      let circle1
      let circle2
      this.addInputClassName = 'input is-rounded'
      this.addInformation = 'add a name for the room'
      // if statement prüft ob der Raum geschlossen wurde
      if (this.canvas.getObjects('circle')[0] && this.canvas.getObjects('circle')[this.canvas.getObjects('circle').length - 1]) {
        circle1 = this.canvas.getObjects('circle')[0] as fabric.Circle
        circle2 = this.canvas.getObjects('circle')[this.canvas.getObjects('circle').length - 1] as fabric.Circle
        if (circle1.top === circle2.top && circle1.left === circle2.left)
          this.modalActive = !this.modalActive
      }
    },
    addNewRoom() {
      if (this.newRoomName.length < 1) {
        this.addInformation = 'Enter a Room name first!!!'
        this.addInputClassName = 'input is-rounded is-danger'
      } else {
        let linesWithoutGrid = this.canvas.getObjects('line').slice(120, this.canvas.getObjects('line').length) as Line[]
        let newRoom = new Room(this.newRoomName, this.canvas.getObjects('circle') as Circle[], linesWithoutGrid)
        this.rooms.push(newRoom)
        this.newRoomName = ''
        this.modalActive = false
        // this.redrawCavas(this.rooms)
      }
    },
    // redrawCavas(existingRooms: Room[]) {
    //   this.canvas.clearRect(0, 0, this.canvasFromView.width, this.canvasFromView.height)
    //   existingRooms.forEach((room) => {
    //     room.points.forEach((point) => {
    //       this.drawExistingPoint(point)
    //     })
    //     this.drawLineBetweenPoints(new Point(0, 0), new Point(0, 0), room.points)
    //   })
    // }
  }
});
</script>

<style lang="scss">

.sketching-board {
  display: grid;
  text-align: center;
}

.modal-container {
  grid-column: 2;
  grid-row: 2;

  .modal-content {
    top: 40px;
    background: #ffffff;
    width: 400px;
    border-radius: 10px;
  }
}

.board {
  grid-column: 2;
  grid-row: 2;
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
.modal-close {
  z-index: 2;
  position: absolute;
}

canvas {
  border: 3px solid black;
  text-align: center;
}
</style>
