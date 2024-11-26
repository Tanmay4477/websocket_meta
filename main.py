from fastapi import FastAPI, WebSocket, WebSocketDisconnect, WebSocketException, status
from fastapi.responses import HTMLResponse
from schema import JoinSpaceSchema
from json import loads
from manager import ConnectionManager
from html import html
from space import RoomManager
from schema import JoinSpaceSchema

app = FastAPI()    
manager = ConnectionManager()
room = RoomManager()

@app.websocket("/")
async def room_implementation(websocket: WebSocket):
    await manager.connect(websocket)
    room_key = str(websocket)
    try:
        while True:
            str_data = await websocket.receive_text()
            data = loads(str_data)
            payload = room.send_data(room_key, data)
            await manager.broadcast(payload["payload1"])
            await manager.send_personal_message(payload["payload2"], websocket)


    except WebSocketDisconnect:
        manager.disconnect(websocket)
        payload = room.user_left(room_key)
        await manager.broadcast(payload["payload1"])


