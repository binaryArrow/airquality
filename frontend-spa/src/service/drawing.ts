import {fabric} from "fabric";
import Room from "@/../../backend/src/models/Room";
import Sensor from "@/../../backend/src/models/Sensor";
import {Circle, Line} from "fabric/fabric-impl";
import CircleWithLine from "@/../../../backend/src/models/CircleWithLine"
import RectWithId from "@/../../../backend/src/models/RectWithId"

export class Drawing {

    static redraw(canvas: fabric.Canvas,
                  rooms: Room[],
                  lengthsOfObjects: {
                      lengthOfCirclesInRooms: number,
                      lengthOfLinesInRooms: number
                  },
                  sensors: Sensor[]) {
        canvas.clear()
        lengthsOfObjects.lengthOfCirclesInRooms = 0
        lengthsOfObjects.lengthOfLinesInRooms = 0
        console.log(`in canvas: ${canvas.getObjects().length}`)
        rooms.forEach(it => {
            it.points.forEach(point => {
                canvas.add(point)
            })
            it.lines.forEach(line => {
                canvas.add(line)
            })
            lengthsOfObjects.lengthOfCirclesInRooms += it.points.length
            lengthsOfObjects.lengthOfLinesInRooms += it.lines.length
        })
        sensors.forEach(sensor => {
            if (sensor.active) {
                const rectangleOptions = {
                    sensorId: sensor.sensorId,
                    width: sensor.width,
                    height: sensor.width,
                    left: sensor.left,
                    top: sensor.top,
                    fill: 'green',
                    stroke: 'black',
                    strokeWidth: 3
                } as RectWithId
                canvas.add(new fabric.Rect(rectangleOptions))
            }
        })
    }

    static drawGrid(width: number, height: number, grid: number, canvas: fabric.Canvas) {
        for (let i = 0; i < (width / grid); i++) {
            canvas.add(new fabric.Line([i * grid, 0, i * grid, height], {
                stroke: '#ccc',
                selectable: false,
                hoverCursor: 'false'
            }));
            canvas.add(new fabric.Line([0, i * grid, width, i * grid], {
                stroke: '#ccc',
                selectable: false,
                hoverCursor: 'false'
            }))
        }
    }

    static makeCircle(left: number, top: number, grid: number, line1?: fabric.Line, line2?: fabric.Line): Circle {
        const opt = {
            left: Math.round(left / grid) * grid,
            top: Math.round(top / grid) * grid,
            radius: 5,
            fill: 'red',
            originX: 'center',
            originY: 'center',
            centeredRotation: true,
            strokeWidth: 2,
            lockRotation: true,
            lockScalingX: true,
            lockScalingY: true,
            line1: line1,
            line2: line2,
            hasControls: false,
            hasBorders: false,
        } as CircleWithLine

        return new fabric.Circle(opt)

    }

    static makeLine(coords: number[]) {
        return new fabric.Line(coords, {
            stroke: 'red',
            strokeWidth: 3,
            lockScalingX: true,
            lockScalingY: true,
        })
    }

    static mapCirclesFromDB(pointsFromDB: string, grid: number): Circle[] {
        const circleArray: Circle[] = []
        const test = JSON.parse(pointsFromDB)
        for (const element of test) {
            const newCircle = this.makeCircle(element.left, element.top, grid)
            newCircle.fill = '#30880DFF'
            newCircle.selectable = false
            circleArray.push(newCircle)
        }
        return circleArray
    }

    static mapLinesFromDB(lineCoordinatesFromDB: string): Line[] {
        const linesArray: Line[] = []
        const test = JSON.parse(lineCoordinatesFromDB)
        for (const element of test) {
            const newLine = this.makeLine([element.x1, element.y1, element.x2, element.y2])
            newLine.stroke = '#30880DFF'
            newLine.selectable = false
            linesArray.push(newLine)
        }
        return linesArray
    }

}