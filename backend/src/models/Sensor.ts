export default class Sensor{
    id?: number
    sensorId: number
    left:number = 0
    top: number = 0
    width: number = 20
    active: boolean = false

    constructor(id: number) {
        this.sensorId = id
    }
}