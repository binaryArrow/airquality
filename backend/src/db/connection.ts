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
                    table.specificType('points', 'object ARRAY')
                    table.specificType('lines', 'object ARRAY')
                    table.specificType('sensor', 'object')
                })
            }
        })
    }

    insertRoom(room: Room) {
        try {
            return this.dbConnection('rooms').insert(room).then(() => {
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