from app.controller.base import BaseController
from app.model.room import Room
from app.schema.room import RoomCreate, RoomUpdate, RoomResponse
from app.service.room_service import room_service

class RoomController(BaseController[Room, RoomCreate, RoomUpdate, RoomResponse]):
    def __init__(self):
        super().__init__(service=room_service, model_name="Room")

room_controller = RoomController()

