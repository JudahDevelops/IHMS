from app.model.room import Room
from app.schema.room import RoomCreate, RoomUpdate
from app.service.base import BaseService

class RoomService(BaseService[Room, RoomCreate, RoomUpdate]):
    def __init__(self):
        super().__init__(
            model=Room,
            search_fields=[Room.room_number]
        )

room_service = RoomService()

