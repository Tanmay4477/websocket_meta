from fastapi import WebSocket, status, WebSocketException
from schema import JoinSpaceSchema
from auth import decode_token

class RoomManager:
    def __init__ (self):
        self.room_data = {}
        self.users_data = {}

    def send_data(self, room_key: str, data: JoinSpaceSchema) -> JoinSpaceSchema:
        if data.get("type") == "join":
            payload = self.join(room_key, data)
        elif data.get("type") == "move":
            payload = self.move(room_key, data)
        elif data.get("type") == "left":
            payload = self.user_left(room_key)
        return payload


    def move(self, room_key: str, data: JoinSpaceSchema) -> JoinSpaceSchema:
        if room_key not in self.users_data:
            payload = {
                "payload1": None,
                "payload2": {
                    "type": "Join the room first"
                }
            }
            return payload
        user_id = self.users_data[room_key][0]
        space_id = self.users_data[room_key][1]

        old_x = self.room_data[space_id][user_id][0]
        old_y = self.room_data[space_id][user_id][1]
        new_x = data["payload"]["x"]
        new_y = data["payload"]["y"]

        if (new_x, new_y) in self.room_data[space_id].values():
            payload = {
                "payload1": None,
                "payload2": {
                    "type": "movement-rejected",
                    "payload": {
                        "x": old_x,
                        "y": old_y
                    }
                }
            }
            return payload
        
        if (new_x, new_y) not in [(old_x, old_y+1), (old_x, old_y-1), (old_x-1, old_y), (old_x+1, old_y)]:
            payload = {
                "payload1": None,
                "payload2": {
                    "type": "movement-rejected",
                    "payload": {
                        "x": old_x,
                        "y": old_y
                    }
                }
            }
            return payload
        
        self.room_data[space_id][user_id] = (new_x, new_y)
        payload = {
            "payload1": {
                "type": "movement",
                "payload": {
                    "x": new_x,
                    "y": new_y,
                    "userId": user_id
                }
            },
            "payload2": None
        }        
        return payload
    
    def join(self, room_key: str, data: JoinSpaceSchema) -> JoinSpaceSchema:
        token = data.get("payload").get("token")
        space_id = data.get("payload").get("spaceId")
        user = decode_token(token)

        if not user:
            raise WebSocketException(code=status.WS_1014_BAD_GATEWAY)

        user_id = user['id']
        desi_space_id = int(space_id)

        if(desi_space_id not in self.room_data):
            self.room_data[desi_space_id] = {}
        
        self.room_data[desi_space_id][user_id] = (2, 1)
        self.users_data[room_key] = (user_id, desi_space_id) 
        
        payload = {
            "payload1": {
                "type": "user-join",
                "payload": {
                    "userId": user_id,
                    "x": 2,
                    "y": 1
                }
            },
            "payload2": {
                "type": "space-joined",
                "payload": {
                    "spawn": {
                        "x": 2,
                        "y": 1
                    },
                "users": self.room_data[desi_space_id]
                }
            }
        }
        return payload
    
    def user_left(self, room_key: str) -> JoinSpaceSchema:
        user = self.users_data[room_key]
        del self.users_data[room_key]
        payload = {
            "payload1": {
	            "type": "user-left",
	            "payload": {
		            "userId": user
	            }
            },
            "payload2": None
        }
        return payload




# room_data = {
#     1: {1: (1, 2), 2: (3, 5), 3: (6, 7)},
#     2: {6: (7, 2), 1: (3, 5), 9: (6, 7)}
# }

#  first key is space id and then the key is x and y and the value is user_id and element_id