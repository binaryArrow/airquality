import express from 'express'
import bodyParser from "body-parser";
import cors from 'cors'
import {createServer} from 'http'
import {Server, Socket} from "socket.io";
import {Connection} from "./db/connection";
import Room from "./models/Room";

const connection = new Connection()
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

app.get('/rooms', async (req, res) => {

    const rooms = await connection.getAllRooms()
    res.status(200).json(rooms)
})
app.post('/rooms', async (req, res) => {
    const response = await connection.insertRoom(req.body as Room)
    res.status(201).json(response)
})
app.delete('/room/:uuid', async (req, res) => {
    await connection.deleteRoom(req.params.uuid)
    res.status(200).json({deleted: true})
})

let data = {
    lineCoords: [10, 10, 20, 20],
    circleLeft: 50,
    circleTop: 50
}


io.on("connection", socket => {
    console.log('new connection!')
    socket.emit("data", data)
})

httpServer.listen(3000, () => console.log('Server running'))


