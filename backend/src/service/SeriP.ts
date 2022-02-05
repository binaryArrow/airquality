const SerialPort = require('serialport')
import {SensorData} from "../models/SensorData";
import {Connection} from "../db/connection";
const Readline = SerialPort.parsers.Readline;

export class SeriP {

    parser: any
    port: any
    dataset?: SensorData
    connection: Connection

    constructor(connection: Connection, portName: any) {

        this.port = new SerialPort(portName, {
            baudRate: 38400,
            dataBits: 8,
            parity: "none",
            stopBits: 1
        })
        console.log("Port created!")
        this.parser = new Readline()
        this.connection = connection
    }

    listen(io: any) {
        this.port.pipe(this.parser)
        this.parser.on('data', async (data?: any) => {
            let recieveArr = data.split(";")                   // split by ";"
            const id: number = +recieveArr[0]                  // save to const & parse string to number
            const tempSHT21 = recieveArr[1]                    // save the rest
            const humSHT21 = recieveArr[2]
            const tempSCD41 = recieveArr[3]
            const humSCD41 = recieveArr[4]
            const co2SCD41 = recieveArr[5]
            const eco2CCS811 = recieveArr[6]
            const tvocCCS811 = recieveArr[7]
            const battery = recieveArr[8]
            this.dataset = new SensorData(id, tempSHT21, humSHT21, tempSCD41, humSCD41, co2SCD41, eco2CCS811, tvocCCS811, battery)    // object to save in db
            console.log('Data:', id, tempSHT21, humSHT21, tempSCD41, humSCD41, co2SCD41, eco2CCS811, tvocCCS811, battery);
            await this.connection.insertSensorData(this.dataset)// save object in database
            io.emit("data", this.dataset)
        })
    }
}


