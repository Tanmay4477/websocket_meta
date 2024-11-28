from fastapi import WebSocket, status, WebSocketException
from schema import JoinSpaceSchema
from auth import decode_token
import json


class RoomManager:
    def __init__(self):
        self.room_data = {}
        self.users_data = {}
        self.connection_data = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, space_id: int):
        for connection in self.connection_data[space_id]:
            await connection.send_text(message)

    async def send_data(self, websocket: WebSocket, data: JoinSpaceSchema):
        if data.get("type") == "join":
            await self.join(websocket, data)
        elif data.get("type") == "move":
            await self.move(websocket, data)
        elif data.get("type") == "left":
            await self.user_left(websocket)

    async def join(self, websocket: WebSocket, data: JoinSpaceSchema):
        token = data.get("payload").get("token")
        space_id = data.get("payload").get("spaceId")
        user = decode_token(token)

        if not user:
            raise WebSocketException(code=status.WS_1014_BAD_GATEWAY)

        user_id = user["id"]
        final_space_id = int(space_id)

        if final_space_id not in self.room_data:
            self.room_data[final_space_id] = {}

        if final_space_id not in self.connection_data:
            self.connection_data[final_space_id] = []

        if websocket in self.connection_data[final_space_id]:
            message6 = json.dumps({
                "type": "already-present"
            })
            await self.send_personal_message(message6, websocket)
            return

        room_key = str(websocket)
        self.room_data[final_space_id][user_id] = (2, 1)
        self.users_data[room_key] = (user_id, final_space_id)
        self.connection_data[final_space_id].append(websocket)

        message = json.dumps({
            "type": "user-join",
            "payload": {
                "userId": user_id,
                "x": 2,
                "y": 1
            }
        })
        await self.broadcast(message, final_space_id)

        message2 = json.dumps({
            "type": "space-joined",
            "payload": {
                "spawn": {
                    "x": 2,
                    "y": 1
                },
                "users": self.room_data[final_space_id]
            }
        })
        await self.send_personal_message(message2, websocket)
        return

    async def user_left(self, websocket: WebSocket):
        room_key = str(websocket)
        user_id = self.users_data[room_key][0]
        space_id = self.users_data[room_key][1]
        self.connection_data[space_id].remove(websocket)

        if len(self.connection_data[space_id]) == 0:
            del self.connection_data[space_id]

        del self.users_data[room_key]
        del self.room_data[space_id][user_id]

        payload = json.dumps({
            "type": "user-left",
            "payload": {
                "userId": user_id
            }
        })
        await self.broadcast(payload, space_id)
        return

    async def move(self, websocket: WebSocket, data: JoinSpaceSchema):
        room_key = str(websocket)
        if room_key not in self.users_data:
            message = json.dumps({
                "type": "Join the room"
            })
            await self.send_personal_message(message, websocket)
            return

        user_id = self.users_data[room_key][0]
        space_id = self.users_data[room_key][1]

        old_x = self.room_data[space_id][user_id][0]
        old_y = self.room_data[space_id][user_id][1]
        print(data)
        new_x = data['payload']['x']
        new_y = data['payload']['y']

        if (new_x, new_y) in self.room_data[space_id].values():
            message2 = json.dumps({
                "type": "movement-rejected",
                "payload": {
                    "x": old_x,
                    "y": old_y
                }
            })
            await self.send_personal_message(message2, websocket)
        elif (new_x, new_y) not in [(old_x, old_y + 1), (old_x, old_y - 1), (old_x - 1, old_y), (old_x + 1, old_y)]:
            message3 = json.dumps({
                "type": "movement-rejected",
                "payload": {
                    "x": old_x,
                    "y": old_y
                }
            })
            await self.send_personal_message(message3, websocket)
        else:
            self.room_data[space_id][user_id] = (new_x, new_y)
            message4 = json.dumps({
                "type": "movement",
                "payload": {
                    "x": new_x,
                    "y": new_y,
                    "userId": user_id
                }
            })
            await self.broadcast(message4, space_id)
            return
