import express from 'express'
import {InfluxConnection} from "./influxData";
import {Point} from "@influxdata/influxdb-client";

const app = express()
const influxConnection: InfluxConnection = new InfluxConnection

let temperaturePoints = new Array<Point>()
let qualityPoints = new Array<Point>()

app.get('/', (req, res) => {

    timedDataCreation(10)

    res.send('Hello World');

})

app.listen(8000, () => console.log('Server running'))

function timedDataCreation(iterations: number) {
    setTimeout(() => {
        let temperaturePoint: Point = new Point('temperature')
            .tag('sensor_id', 'S01')
            .floatField('value', iterations)
        influxConnection.writePoint(temperaturePoint)
        if (--iterations) timedDataCreation(iterations)
    }, 1000)
}