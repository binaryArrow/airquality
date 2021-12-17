import express from 'express'
import {createServer} from 'http'
import {Server, Socket} from "socket.io";
import {Connection} from "./db/connection";

const connection = new Connection()
const app = express()
const httpServer = createServer(app)
const io = new Server(httpServer, {
    cors: {
        origin: "*"
    }
})

app.get('/', (req, res) => {

    res.send('Hello World');
    connection.testInsert()

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


