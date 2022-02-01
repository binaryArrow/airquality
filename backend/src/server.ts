import express from 'express'
import bodyParser from "body-parser";
import cors from 'cors'
import {createServer} from 'http'
import {Server, Socket} from "socket.io";
import {Connection} from "./db/connection";
import Room from "./models/Room";
import {SensorData} from "./models/SensorData";
import {SeriP} from "./service/SeriP";
import Sensor from "./models/Sensor";
import SerialPort from "serialport";

const connection = new Connection()
let checkInterval = 1000
let portName = ""
let waitForZigBee: NodeJS.Timer
const app = express()
app.use(bodyParser.urlencoded({extended: false}))
app.use(bodyParser.json())
app.use(cors())
const httpServer = createServer(app)
const io = new Server(httpServer, {
    cors: {
        origin: "*"
    }
})

app.get('/rooms', async (req: any, res: any) => {
    const rooms = await connection.getAllRooms()
    res.status(200).json(rooms)
})
app.get('/sensordata/:sensorId/:amount', async (req: any, res: any )=>{
    const sensordata = await connection.getSensorData(req.params.sensorId, req.params.amount)
    res.status(200).json(sensordata)
})
app.post('/rooms', async (req: any, res: any) => {
    const response = await connection.insertRoom(req.body)
    const idResponse = await connection.getLastRoom()
    res.contentType('application/json')
    res.status(201)
    res.json(idResponse)
})
app.put('/rooms/:roomId/:sensorId', async (req: any, res: any) => {
    const update = await connection.updateRoomSensorid(req.params.roomId, req.params.sensorId)
    res.status(200)
    res.json(update)
})
app.delete('/room/:id', async (req: any, res: any) => {
    await connection.deleteRoom(req.params.id)
    res.status(200).json({deleted: true})
})
app.get('/sensors', async (req: any, res: any) => {
    const sensors = await connection.getSensors()
    res.status(200).json(sensors)
})
app.put('/sensors', async (req: any, res: any) => {
    const sensors = req.body as Sensor[]
    connection.updateSensors(sensors)
    res.status(200)
    res.json(sensors)
})

httpServer.listen(3000, () => {
    waitForZigBee = setInterval(getPortName, checkInterval)
    console.log('Server running')
})

function getPortName(){
    if(portName == ""){
        SerialPort.list().then(async(ports?: any, err?: any) =>{
            for (const port of ports) {
                if(port.manufacturer.includes('FTDI') && port.vendorId.includes('0403')){
                    portName = port.path
                    console.log("Port found:", portName)
                }
            }
        })
    }else{
        clearInterval(waitForZigBee)
        const serial = new SeriP(connection, portName)
        serial.listen(io)
        serial.port.on('close', async (err?: any) => {
            console.log("Port closed.");
            if (err.disconnected) {
                console.log("Disconnected!");
                portName = ""
                waitForZigBee = setInterval(getPortName, checkInterval)
            }
        });
    }
}