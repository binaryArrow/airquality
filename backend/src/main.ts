import express from 'express'
import {InfluxConnection} from "./influxData";
import {Point} from "@influxdata/influxdb-client";

const app = express()

app.get('/', (req, res) => {
    const influxConnection: InfluxConnection = new InfluxConnection

    let temperaturePoints = new Array<Point>()
    let qualityPoints = new Array<Point>()

    for(let i = 3; i <= 10; i++){
        let temperaturePoint: Point = new Point('temperature')
            .tag('sensor_id', 'S01')
            .floatField('value', i)
        temperaturePoints.push(temperaturePoint)

        let qualityPoint: Point = new Point('quality')
            .tag('sensor_id', 'S01')
            .floatField('value', i + 20)
        qualityPoints.push(qualityPoint)

    }
    influxConnection.writePoints(temperaturePoints)
    influxConnection.writePoints(qualityPoints)

    res.send('Hello World');

})

app.listen(8000, () => console.log('Server running'))

