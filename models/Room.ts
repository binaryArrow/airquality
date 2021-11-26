import {Sensor} from "./Sensor";

export class Room {
    roomName: string
    sensor: Sensor
    constructor(name: string, sensor: Sensor) {
        this.roomName = name
        this.sensor = sensor
    }
}