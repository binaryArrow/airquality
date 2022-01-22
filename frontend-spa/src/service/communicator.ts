import Room from "@/../../backend/src/models/Room";
import Sensor from "@/../../backend/src/models/Sensor";

export class Communicator {
    async getRooms(): Promise<Room[]> {
        return fetch('http://localhost:3000/rooms', {
            method:'GET',
            headers: {'Content-Type': 'application/json'}
        })
            .then(res => res.json())
            .catch(e => console.log(e.message))
    }
    async postRoom(room: Room): Promise<any> {
        return fetch('http://localhost:3000/rooms', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(room)
        })
            .then((res) => res.json())
            .catch(e => console.log(e.message))
    }
    async updateRoomSensorId(roomId: number, sensorId: number): Promise<any>{
        return fetch(`http://localhost:3000/rooms/${roomId.toString()}/${sensorId.toString()}`, {
            method:'PUT'
        })
            .then((res) => res.json())
            .catch(e => console.log(e.message))
    }
    async deleteRoom(id?: number): Promise<any> {
        if(!id){
            return new Error("no ID of room to delete")
        }
        return fetch(`http://localhost:3000/room/${id.toString()}`, {
            method: 'DELETE'
        })
    }
    async getSenors(): Promise<Sensor[]> {
        return fetch('http://localhost:3000/sensors', {
            method:'GET',
            headers: {'Content-Type': 'application/json'}
        })
            .then(res => res.json())
            .catch(e => console.log(e.message))
    }
    async updateSensorsInBackend(sensor: Sensor[]): Promise<any>{
        return fetch(`http://localhost:3000/sensors`, {
            method:'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(sensor)
        })
            .then((res) => res.json())
            .catch(e => console.log(e.message))
    }


}