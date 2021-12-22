import {fabric} from "fabric";

export default interface CircleWithLine extends fabric.Object, fabric.Circle {
    line1?: fabric.Line,
    line2?: fabric.Line,
}