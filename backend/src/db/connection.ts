import knex from 'knex'

export class Connection{
    private dbConnection

    constructor() {
        this.dbConnection = knex({
            client: 'sqlite3',
            connection:{
                filename: `${__dirname}/testDB.db`
            },
            useNullAsDefault: true
        })
    }

    testInsert() {
        return this.dbConnection("human").insert({name: "test"}).then(()=>{
            console.log("wrote")
        })
    }
}