import Sensor from "./Sensor";
import {v4, v4 as uuidv4} from 'uuid'
import {fabric} from "fabric";
import LineCoords from "./lineCoords";

export default class Room {
    id?: number
    uuid: string
    roomName: string
    points: fabric.Circle[]
    lines: fabric.Line[]
    lineCoords: LineCoords[]
    sensor: Sensor
    constructor(name: string, points: fabric.Circle[], lines: fabric.Line[], sensor: Sensor, lineCoords: LineCoords[], id?: number) {
        this.id = id
        this.uuid = uuidv4()
        this.roomName = name
        this.sensor = sensor
        this.points = points
        this.lines = lines
        this.sensor = sensor
        this.lineCoords = lineCoords
    }
}