import {Sensor} from "./Sensor";
import Point from "./Point";

export default class Room {
    roomName: string
    point?: Point[]
    sensor: Sensor
    constructor(name: string, sensor: Sensor) {
        this.roomName = name
        this.sensor = sensor
    }
}