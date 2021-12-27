<template>
  <div class="sketching-board">
    <div class="board">
      <canvas ref="drawingCanvas" :width="width" :height="height"></canvas>
    </div>
    <div class="modal-container">
      <add-modal :is-active="addModalActive">
        <div class="modal-content">
          <p><b>{{ addInformation }}</b></p>
          <input v-bind:class="addInputClassName" type="text" v-model="newRoomName" placeholder="Room name">
          <button class="button is-success" @click="addNewRoom">ADD</button>
          <button class="button is-danger" @click="toggleModal('add')">CANCEL</button>
        </div>
      </add-modal>
      <list-modal class="modal-content" :is-active="listModalActive" :rooms="this.rooms"
                  @delete-room="deleteSelectedRoom"
                  @close="toggleModal"
      @sensor-added="sensorAdded">
      </list-modal>
    </div>
  </div>
  <div class="add-button-wrapper">
    <button id="add-button" class="button is-primary" @click="toggleModal('add')" v-show="!addModalActive"
            type="button">ADD
      ROOM
    </button>
    <button id="list-button" class="button is-warning" @click="toggleModal('list')" v-show="!listModalActive"
            type="button">SHOW ROOMS
    </button>
  </div>
</template>

<script lang="ts">
import {defineComponent, ref} from 'vue';
import Room from "@/../../backend/src/models/Room";
import Sensor from "@/../../backend/src/models/Sensor";
import AddModal from '@/components/AddModal.vue'
import {fabric} from "fabric";
import {Circle, Line} from "fabric/fabric-impl";
import ListModal from "@/components/ListModal.vue";
import {io} from "socket.io-client";
import {Communicator} from "@/service/communicator";
import {Drawing} from "@/service/drawing";
import CircleWithLine from "@/../../../backend/src/models/CircleWithLine"
import LineCoords from '../../../backend/src/models/LineCoords';

const socket = io("http://localhost:3000")

export default defineComponent({
  name: 'SketchingBoard',

  components: {
    ListModal,
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
      addModalActive: ref(false),
      listModalActive: ref(false),
      newRoomName: '',
      addInformation: 'add a name for the room',
      addInputClassName: 'input is-rounded',
      lengthsOfObjects: {
        lengthOfCirclesInRooms: 0,
        lengthOfLinesInRooms: 0
      },
      communicator: new Communicator()
    }
  },
  mounted() {
    this.canvasFromView = this.$refs['drawingCanvas'] as HTMLCanvasElement
    this.canvas = new fabric.Canvas(this.canvasFromView)
    this.canvas.selection = false

    this.communicator.getRooms().then(data => {
      console.log(data)
      data.forEach(room => {
        let newRoom = new Room(
            room.roomName,
            Drawing.mapCirclesFromDB(room.points.toString(), this.grid),
            Drawing.mapLinesFromDB(room.lineCoords.toString()),
            room.sensorId,
            room.lineCoords,
            room.id
        )
        this.rooms.push(newRoom)
      })
      console.log(this.rooms)
      Drawing.redraw(this.canvas, this.rooms, this.lengthsOfObjects)
      Drawing.drawGrid(this.width, this.height, this.grid, this.canvas)
    })
    socket.on("data", (data: { lineCoords: number[]; circleLeft: number; circleTop: number }) => {
      console.log("got some data from socket")
    })
    Drawing.drawGrid(this.width, this.height, this.grid, this.canvas)


    // canvas methods
    this.canvas.on('selection:created', (event) => {
      if (event.target)
        event.target.set({
          lockScalingY: true,
          lockScalingX: true
        })
    })
    this.canvas.on("mouse:dblclick", (options) => {
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
    addPoint() {
      let newPoint = Drawing.makeCircle(this.mousePosX, this.mousePosY, this.grid)
      let newLine
      this.canvas.add(newPoint)
      console.log(`in rooms: ${this.lengthsOfObjects.lengthOfCirclesInRooms} < ${(this.canvas.getObjects('circle').length - 1)}`)
      if (this.canvas.getObjects('circle').length >= 2 && (this.lengthsOfObjects.lengthOfCirclesInRooms < this.canvas.getObjects('circle').length - 1)) {
        newLine = Drawing.makeLine([
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
      console.log("Circles in canvas: ")
      console.log(this.canvas.getObjects('circle'))
    },
    toggleModal(type: string) {
      switch (type) {
        case "add": {
          let circle1
          let circle2
          this.addInputClassName = 'input is-rounded'
          this.addInformation = 'add a name for the room'
          // if statement prüft ob der Raum geschlossen wurde
          console.log(this.canvas.getObjects('circle')[this.lengthsOfObjects.lengthOfCirclesInRooms])
          console.log(this.canvas.getObjects('circle')[this.canvas.getObjects('circle').length - 1])
          if (this.canvas.getObjects('circle')[this.lengthsOfObjects.lengthOfCirclesInRooms] && this.canvas.getObjects('circle')[this.canvas.getObjects('circle').length - 1]) {
            circle1 = this.canvas.getObjects('circle')[this.lengthsOfObjects.lengthOfCirclesInRooms] as fabric.Circle
            circle2 = this.canvas.getObjects('circle')[this.canvas.getObjects('circle').length - 1] as fabric.Circle
            if (circle1.top === circle2.top && circle1.left === circle2.left)
              this.addModalActive = !this.addModalActive
          }
          break;
        }
        case "list": {
          this.listModalActive = !this.listModalActive
        }
      }
    },
    addNewRoom() {
      if (this.newRoomName.length < 1) {
        this.addInformation = 'Enter a Room name first!!!'
        this.addInputClassName = 'input is-rounded is-danger'
      } else {
        this.canvas.getObjects().slice((this.width / this.grid) * 2, this.canvas.getObjects().length).forEach(it => it.set('fill', '#30880d'))
        this.canvas.getObjects().forEach(it => it.set("selectable", false))
        this.canvas.getObjects('line').splice((this.width / this.grid) * 2, this.canvas.getObjects('line').length).forEach((it) => {
          it.stroke = '#30880d'
        })
        let linesWithoutGrid = this.canvas.getObjects('line').slice((this.width / this.grid) * 2 + this.lengthsOfObjects.lengthOfLinesInRooms, this.canvas.getObjects('line').length) as Line[]
        let lineCoordinates: LineCoords[] = []
        linesWithoutGrid.forEach(line => {
          lineCoordinates.push({
            x1: line.x1 as number,
            x2: line.x2 as number,
            y1: line.y1 as number,
            y2: line.y2 as number })
        })
        let newRoom = new Room(
            this.newRoomName,
            this.canvas.getObjects('circle').slice(this.lengthsOfObjects.lengthOfCirclesInRooms, this.canvas.getObjects('circle').length) as Circle[],
            linesWithoutGrid,
            0,
            lineCoordinates
        )
        this.communicator.postRoom(newRoom).then((data: [{'max(`id`)': 27}]) => {
          data.forEach(id => {
            newRoom.id = id["max(`id`)"]
          })
        })
        this.rooms.push(newRoom)
        this.newRoomName = ''
        this.addModalActive = false
        Drawing.redraw(this.canvas, this.rooms, this.lengthsOfObjects)
        Drawing.drawGrid(this.width, this.height, this.grid, this.canvas)
      }
    },
    deleteSelectedRoom(index: number) {
      this.communicator.deleteRoom(this.rooms[index].id)
      this.rooms.splice(index, 1)
      Drawing.redraw(this.canvas, this.rooms, this.lengthsOfObjects)
      Drawing.drawGrid(this.width, this.height, this.grid, this.canvas)
    },
    sensorAdded(roomId: number, sensorId: number){
      this.communicator.updateRoomSensorId(roomId, sensorId)
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
  grid-column: 2;
  grid-row: 2;

  .modal-content {
    top: 40px;
    background: #ffffff;
    width: 400px;
    border-radius: 10px;
    border: 2px solid black;
  }
}

.button {
  margin: 5px;
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

  #list-button {
    width: 120px;
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
