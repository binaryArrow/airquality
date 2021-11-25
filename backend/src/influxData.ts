import {InfluxDB, Point, WriteApi} from '@influxdata/influxdb-client'

export class InfluxConnection{
    token: string
    org: string
    bucket: string
    client: InfluxDB
    writeApi: WriteApi
    constructor() {
        this.token = 'fQW5nbFGlYscP051Urvl1orhEOENA-one_r5zgVIbl_BSvian9kDUKlge00I5_lJ0M7rRJoFfLWXdsuRxEXXVA=='
        this.org = 'AirqualityPT'
        this.bucket = 'airquality'
        this.client = new InfluxDB({url: 'http://localhost:8086', token: this.token})
        this.writeApi = this.client.getWriteApi(this.org, this.bucket)
        this.writeApi.useDefaultTags({host: 'host1'})
    }

    writePoint(point: Point){
        this.writeApi.writePoint(point)
        // with close() the connection closes and timed writes don't resolve
        // TODO: maybe close connection on fullfillmend
        this.writeApi.flush().then(() => {
            console.log('WRITE of one point DONE')
        })
    }
    writePoints(points: Point[]){
        this.writeApi.writePoints(points)
        this.writeApi.close().then(()=>{
            console.log(`WRITE of ${points.length} points DONE`)
        })
    }


}