from pydantic import BaseModel
from enum import Enum
from typing import List

class typeWebSocket(str, Enum):
    user_left = "user-left"
    join = "join"
    move = "move"
    space_joined = "space-joined"
    movement_rejected = "movement-rejected"
    movement = "movement"
    user_join = "user-join"

class LeavePayloadSchema(BaseModel):
    userId: int

class MovementPayloadSchema(BaseModel):
    x: int
    y: int 
    userId: int

#  to check as may be userId(not user_id) can create a problem

class MovementRejectPayloadSchema(BaseModel):
    x: int
    y: int

class JoinPayloadSchema(BaseModel):
    spaceId: int
    token: str

class SpaceJoinSchema(BaseModel):
    spawn: MovementRejectPayloadSchema
    users: List[MovementPayloadSchema]

class JoinSpaceSchema(BaseModel):
    type: typeWebSocket
    payload: JoinPayloadSchema | MovementPayloadSchema | MovementRejectPayloadSchema | LeavePayloadSchema | SpaceJoinSchema





