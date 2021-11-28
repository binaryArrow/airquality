import Sensor from "./Sensor";
import Point from "./Point";
import { v4 as uuidv4 } from 'uuid'

export default class Room {
    uuid: string
    roomName: string
    points: Point[]
    sensor?: Sensor
    constructor(name: string, points: Point[], sensor?: Sensor) {
        this.uuid = uuidv4()
        this.roomName = name
        this.sensor = sensor
        this.points = points
    }
}