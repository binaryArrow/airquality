import {fabric} from "fabric";
import Room from "@/../../backend/src/models/Room";
import {Circle} from "fabric/fabric-impl";
import CircleWithLine from "@/../../backend/src/models/circleWithLine"

export class Drawing {

    static redraw(canvas: fabric.Canvas,
                  rooms: Room[],
                  lengthsOfObjects: {
                      lengthOfCirclesInRooms: number,
                      lengthOfLinesInRooms: number
                  }) {
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

}