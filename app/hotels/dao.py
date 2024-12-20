from app.bookings import models
from app.hotels.rooms.models import Rooms
from app.reposit.base import BaseReposit
from app.hotels.models import Hotels
from datetime import date
from app.database import async_sessionmaker
from sqlalchemy import select, and_, or_, func, insert
from app.hotels.models import Hotels
from sqlalchemy import cast, Text

class HotelsDAO(BaseReposit):
    model = Hotels

    @classmethod
    async def find_all_hotels(
        cls,
        date_from: date,
        date_to: date,
    ):
        """
        WITH booked_rooms AS (
            SELECT room_id
            FROM bookings
            WHERE (date_from < '2023-06-20' AND date_to > '2023-05-15') -- Пересечение дат
        )
        SELECT 
            hotels.id,
            hotels.name,
            hotels.location,
            hotels.services::TEXT,
            hotels.rooms_quantity,
            hotels.image_id,
            (hotels.rooms_quantity - COUNT(booked_rooms.room_id)) AS rooms_left
        FROM hotels
        LEFT JOIN rooms ON rooms.hotel_id = hotels.id
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        GROUP BY 
            hotels.id,
            hotels.name,
            hotels.location,
            hotels.services::TEXT,
            hotels.rooms_quantity,
            hotels.image_id
        HAVING (hotels.rooms_quantity - COUNT(booked_rooms.room_id)) > 0;
        """
        async with async_sessionmaker() as session:
            booked_rooms = select(models.Bookings.room_id).where(
                and_(
                    models.Bookings.date_from < date_to,
                    models.Bookings.date_to > date_from
                )
            ).alias("booked_rooms")
            get_rooms_left = select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.rooms_quantity,
                Hotels.image_id,
                (Hotels.rooms_quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
            ).select_from(Hotels).join(
                Rooms, Rooms.hotel_id == Hotels.id, isouter=True
            ).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).group_by(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                cast(Hotels.services, Text),
                Hotels.rooms_quantity,
                Hotels.image_id
            ).having(
                (Hotels.rooms_quantity - func.count(booked_rooms.c.room_id)) > 0
            )

            hotels = await session.execute(get_rooms_left)
            hotels = hotels.mappings().all()
            return hotels
        

    @classmethod
    async def find_all_hotels_rooms(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        async with async_sessionmaker() as session:
            booked_rooms = select(models.Bookings.room_id).where(
                and_(
                    models.Bookings.date_from < date_to,
                    models.Bookings.date_to > date_from
                )
            ).alias("booked_rooms")
            get_hotel_rooms = select(
                Rooms.id,
                Rooms.hotel_id,
                Rooms.name,
                Rooms.description,
                Rooms.services,
                Rooms.price,
                Rooms.quantity,
                Rooms.image_id,
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left"),
                (Rooms.price * (date_to - date_from).days).label("total_cost")
            ).select_from(Rooms).outerjoin(
                booked_rooms, booked_rooms.c.room_id == Rooms.id
            ).where(
                Rooms.hotel_id == hotel_id
            ).group_by(
                Rooms.id,
                Rooms.hotel_id,
                Rooms.name,
                Rooms.description,
                cast(Rooms.services, Text),
                Rooms.price,
                Rooms.quantity,
                Rooms.image_id,
            ).having(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)) > 0
            )

            result = await session.execute(get_hotel_rooms)
            return result.mappings().all()