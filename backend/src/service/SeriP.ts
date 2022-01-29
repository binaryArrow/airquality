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
            this.dataset = new SensorData(id, tempSHT21, humSHT21, tempSCD41, humSCD41, co2SCD41, eco2CCS811, tvocCCS811)    // object to save in db
            console.log('Data:', id, tempSHT21, humSHT21, tempSCD41, humSCD41, co2SCD41, eco2CCS811, tvocCCS811);
            await this.connection.insertSensorData(this.dataset)// save object in database
            io.emit("data", this.dataset)
        })

        /*
        function decode_utf8(s: any) {              // Funktion zum decodieren von UTF-8, falls benötigt sein sollte
            return decodeURIComponent(escape(s));
        }
        */

    function showPortOpen(){
            console.log("Port opened")
    }

    }

}


//const config = require(__dirname + "/SensorData.ts")
//import SensorData from './SensorData'
//import {SensorData} from "../models/SensorData";
//connection.insertSensorData(sensId)