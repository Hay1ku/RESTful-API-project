from app.reposit.base import BaseReposit
from app.hotels.rooms.models import Rooms

class RoomsDAO(BaseReposit):
    model = Rooms