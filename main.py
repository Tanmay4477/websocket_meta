from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from space import RoomManager

app = FastAPI()    
room = RoomManager()

@app.websocket("/")
async def room_implementation(websocket: WebSocket):
    await room.connect(websocket)
    try:
        while True:
            str_data = await websocket.receive_text()
            data = json.loads(str_data)
            await room.send_data(websocket, data)

    except WebSocketDisconnect:
        await room.user_left(websocket)
      


