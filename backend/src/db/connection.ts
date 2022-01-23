import knex from 'knex'
import Room from "../models/Room";
import {SensorData} from "../models/SensorData";
import Sensor from "../models/Sensor";

export class Connection {
    private dbConnection: any

    constructor() {
        this.dbConnection = knex({
            client: 'sqlite3',
            connection: {
                filename: `${__dirname}/testDB.db`
            },
            useNullAsDefault: true
        })
        this.dbConnection.schema.hasTable('rooms').then((exists: boolean) => {
            if (!exists) {
                return this.dbConnection.schema.createTable('rooms', (table: any) => {
                    table.increments('id')
                    table.string('roomName')
                    table.string('points')
                    table.string('lines')
                    table.string('lineCoords')
                    table.integer('sensorId')
                    table.timestamp('created_at').defaultTo(this.dbConnection.fn.now())
                })
            }
        })
        this.dbConnection.schema.hasTable('sensor-data').then((exists: boolean) => {
            if (!exists) {
                return this.dbConnection.schema.createTable('sensor-data', (table: any) => {
                    table.increments('id')
                    table.integer('sensorId')
                    table.integer('roomId')
                    table.string('tempSHT21')
                    table.string('humSHT21')
                    table.string('tempSCD41')
                    table.string('humSCD41')
                    table.string('co2SCD41')
                    table.string('eco2CCS811')
                    table.string('tvocCCS811')
                    table.timestamp('created_at').defaultTo(this.dbConnection.fn.now())
                })
            }
        })
        this.dbConnection.schema.hasTable('sensors').then((exists: boolean) => {
            if (!exists) {
                return this.dbConnection.schema.createTable('sensors', (table: any) => {
                    table.increments('id')
                    table.integer('sensorId')
                    table.integer('left')
                    table.integer('top')
                    table.integer('width')
                    table.boolean('active')
                }).then(() => {
                    this.insertSensors(1)
                    this.insertSensors(2)
                    this.insertSensors(3)
                })
            }
        })
    }

    insertSensors(sensorId: number) {
        try {
            return this.dbConnection('sensors').insert({
                sensorId: sensorId,
                left: 0,
                top: 0,
                width: 20,
                active: false
            }).then(() => {
                console.log('added sensors in Database')
            })
        } catch (e) {
            console.log(`${e}`)
        }
    }

    updateSensors(sensors: Sensor[]) {
        try {
            sensors.forEach(sensor => {
                this.dbConnection('sensors').where('sensorId', sensor.sensorId)
                    .update({
                        left: sensor.left,
                        top: sensor.top,
                        width: sensor.width,
                        active: sensor.active
                    }).then(() => {
                    console.log("sensors updated")
                })
            })
            return this.dbConnection('sensors')
        } catch (e) {
            console.log(`${e}`)
        }
    }

    getSensors() {
        try {
            return this.dbConnection('sensors').select('*')
        } catch (e) {
            console.log(`${e}`)
        }
    }

    insertRoom(room: Room) {
        try {
            return this.dbConnection('rooms').insert({
                roomName: room.roomName,
                points: JSON.stringify(room.points),
                lines: JSON.stringify(room.lines),
                sensorId: JSON.stringify(room.sensorId),
                lineCoords: JSON.stringify(room.lineCoords),
                created_at: this.dbConnection.fn.now()

            }).then(() => {
                console.log("wrote")
            })
        } catch (e) {
            console.log(`${e}`)
        }
    }

    updateRoomSensorid(roomId: number, sensorId: number) {
        try {
            return this.dbConnection('rooms').where('id', roomId).update('sensorId', sensorId)
                .then(() => {
                    console.log("updated room with new Sensor")
                })
        } catch (e) {
            console.log(`${e}`)
        }
    }

    getAllRooms() {
        try {
            return this.dbConnection('rooms').select('*')
        } catch (e) {
            console.log(`${e}`)
        }
    }

    deleteRoom(id: string) {
        try {
            return this.dbConnection('rooms').where('id', id).del().then(() => {
                    console.log("deleted from DB")
                }
            )
        } catch (e) {
            console.log(`${e}`)
        }
    }

    getLastRoom() {
        try {
            return this.dbConnection('rooms').max('id')
        } catch (e) {
            console.log(`${e}`)
        }
    }

    async insertSensorData(sensorData: SensorData) {
        // sensordaten werden nur geschrieben, wenn auch eine verbindung zu einem raum besteht
        let roomIdWithSameSensorId = await this.dbConnection('rooms')
            .where('sensorId', sensorData.sensorId)
            .first()
            .then((row: any) => row)
        if (!roomIdWithSameSensorId) {
            roomIdWithSameSensorId = {id: 0}
        }
        try {
            return this.dbConnection('sensor-data').insert({
                sensorId: sensorData.sensorId,
                roomId: roomIdWithSameSensorId.id,
                tempSHT21: sensorData.tempSHT21,
                humSHT21: sensorData.humSHT21,
                tvocCCS811: sensorData.tvocCCS811,
                eco2CCS811: sensorData.eco2CCS811,
                humSCD41: sensorData.humSCD41,
                tempSCD41: sensorData.tempSCD41,
                co2SCD41: sensorData.co2SCD41,
                created_at: this.dbConnection.fn.now()
            }).then(() => {
                console.log(`wrote sensordata with roomId: ${roomIdWithSameSensorId.id}`)
            })
        } catch (e) {
            console.log(`${e}`)
        }
    }
}