from pydantic import BaseModel
from datetime import date
from typing import List


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int
    rooms_left: int
    date_from: date
    date_to: date