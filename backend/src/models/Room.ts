import Sensor from "./Sensor";
import {fabric} from "fabric";
import LineCoords from "./LineCoords";
import {SensorData} from "./SensorData";

export default class Room {
    id?: number
    roomName: string
    points: fabric.Circle[]
    lines: fabric.Line[]
    lineCoords: LineCoords[]
    sensorId: number
    sensorData?: SensorData[] = []
    constructor(name: string, points: fabric.Circle[], lines: fabric.Line[], sensorId: number, lineCoords: LineCoords[], id?: number) {
        this.id = id
        this.roomName = name
        this.sensorId = sensorId
        this.points = points
        this.lines = lines
        this.lineCoords = lineCoords
    }
}