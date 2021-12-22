export class SensorData {
    sensorId: number
    roomId?: number
    sensorData1?: string
    sensorData2?: string
    sensorData3?: string

    constructor(sensorId: number) {
        this.sensorId = sensorId
    }
}
