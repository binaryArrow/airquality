import {fabric} from "fabric";

export default interface RectWithId extends fabric.Object, fabric.Rect {
    sensorId?: number
}