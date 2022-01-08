export class SensorData {
    sensorId: number
    roomId?: number
    tempSHT21?: string
    humSHT21?: string
    tvocCCS811?: string
    eco2CCS811?: string
    humSCD41?: string
    tempSCD41?: string
    co2SCD41?: string


    constructor(sensorId: number, tempSHT21: string, humSHT21: string, tvocCCS811: string, eco2CCS811: string, humSCD41: string, tempSCD41: string, co2SCD41: string ) {
        this.sensorId = sensorId
        this.tempSHT21 = tempSHT21
        this.humSHT21 = humSHT21
        this.tvocCCS811 = tvocCCS811
        this.eco2CCS811 = eco2CCS811
        this.humSCD41 = humSCD41
        this.tempSCD41 = tempSCD41
        this.co2SCD41 = co2SCD41
    }
}
