import Sensor from "./Sensor";
import { v4 as uuidv4 } from 'uuid'
import {fabric} from "fabric";

export default class Room {
    uuid: string
    roomName: string
    points: fabric.Circle[]
    lines: fabric.Line[]
    sensor: Sensor
    volume?: number
    constructor(name: string, points: fabric.Circle[], lines: fabric.Line[], sensor: Sensor) {
        this.uuid = uuidv4()
        this.roomName = name
        this.sensor = sensor
        this.points = points
        this.lines = lines
        this.sensor = sensor
    }
}