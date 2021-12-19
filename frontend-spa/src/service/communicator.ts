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
    }
}