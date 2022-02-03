"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const body_parser_1 = __importDefault(require("body-parser"));
const cors_1 = __importDefault(require("cors"));
const http_1 = require("http");
const socket_io_1 = require("socket.io");
const connection_1 = require("./db/connection");
const SeriP_1 = require("./service/SeriP");
const serialport_1 = __importDefault(require("serialport"));
const connection = new connection_1.Connection();
let checkInterval = 1000;
let portName = "";
let waitForZigBee;
const app = (0, express_1.default)();
app.use(body_parser_1.default.urlencoded({ extended: false }));
app.use(body_parser_1.default.json());
app.use((0, cors_1.default)());
const httpServer = (0, http_1.createServer)(app);
const io = new socket_io_1.Server(httpServer, {
    cors: {
        origin: "*"
    }
});
app.get('/rooms', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const rooms = yield connection.getAllRooms();
    res.status(200).json(rooms);
}));
app.get('/sensordata/:sensorId/:amount', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const sensordata = yield connection.getSensorData(req.params.sensorId, req.params.amount);
    res.status(200).json(sensordata);
}));
app.post('/rooms', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const response = yield connection.insertRoom(req.body);
    const idResponse = yield connection.getLastRoom();
    res.contentType('application/json');
    res.status(201);
    res.json(idResponse);
}));
app.put('/rooms/:roomId/:sensorId', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const update = yield connection.updateRoomSensorid(req.params.roomId, req.params.sensorId);
    res.status(200);
    res.json(update);
}));
app.delete('/room/:id', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    yield connection.deleteRoom(req.params.id);
    res.status(200).json({ deleted: true });
}));
app.get('/sensors', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const sensors = yield connection.getSensors();
    res.status(200).json(sensors);
}));
app.put('/sensors', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const sensors = req.body;
    connection.updateSensors(sensors);
    res.status(200);
    res.json(sensors);
}));
httpServer.listen(3000, () => {
    waitForZigBee = setInterval(getPortName, checkInterval);
    console.log('Server running');
});
function getPortName() {
    if (portName == "") {
        serialport_1.default.list().then((ports, err) => __awaiter(this, void 0, void 0, function* () {
            for (const port of ports) {
                if (port.manufacturer.includes('FTDI') && port.vendorId.includes('0403')) {
                    portName = port.path;
                    console.log("Port found:", portName);
                }
            }
        }));
    }
    else {
        clearInterval(waitForZigBee);
        const serial = new SeriP_1.SeriP(connection, portName);
        serial.listen(io);
        serial.port.on('close', (err) => __awaiter(this, void 0, void 0, function* () {
            console.log("Port closed.");
            if (err.disconnected) {
                console.log("Disconnected!");
                portName = "";
                waitForZigBee = setInterval(getPortName, checkInterval);
            }
        }));
    }
}
