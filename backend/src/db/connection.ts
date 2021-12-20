import knex from 'knex'
import Room from "../models/Room";

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
                    table.string('uuid')
                    table.string('roomName')
                    table.string('points')
                    table.string('lines')
                    table.string('sensor')
                    table.timestamp('created_at').defaultTo(this.dbConnection.fn.now())
                })
            }
        })
    }

    insertRoom(room: Room) {
        try {
            return this.dbConnection('rooms').insert({
                uuid: room.uuid,
                roomName: room.roomName,
                points: JSON.stringify(room.points),
                lines: JSON.stringify(room.lines),
                sensor: JSON.stringify(room.sensor),
                created_at: this.dbConnection.fn.now()

            }).then(() => {
                console.log("wrote")
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
            return this.dbConnection('rooms').where('uuid', id).del()
        } catch (e) {
            console.log(`${e}`)
        }
    }
}