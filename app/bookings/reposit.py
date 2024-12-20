from datetime import date
from fastapi import HTTPException
from app.database import async_sessionmaker
from app.bookings import models
from sqlalchemy import select, and_, or_, func, insert, delete
from sqlalchemy.orm import aliased
from app.reposit.base import BaseReposit
from app.hotels.rooms.models import Rooms
from app.app_main.excepts import BookingNotFound


class BookingReposit(BaseReposit):
    model = models.Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """
        WITH booked_rooms AS(
        SELECT * FROM bookings
        WHERE room_id = 1 AND 
        (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR 
        (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) AS ostalos_rooms
        FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        async with async_sessionmaker() as session:   
            booked_rooms = select(models.Bookings).where(
                and_(
                    models.Bookings.room_id == 1,
                    or_(
                        and_(
                            models.Bookings.date_from >= date_from,
                            models.Bookings.date_from <= date_to
                        ),
                        and_(
                            models.Bookings.date_from <= date_from,
                            models.Bookings.date_to > date_from
                        )
                    )
                )
            ).cte("booked_rooms")
            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
                                ).select_from(Rooms).join(
                                    booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter= True
                                ).where(Rooms.id == room_id).group_by(
                                    Rooms.quantity, booked_rooms.c.room_id
                                )
            rooms_left = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price = price.scalar()
                add_bookings = insert(models.Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(models.Bookings)

                new_booking = await session.execute(add_bookings)
                await session.commit()
                return new_booking.scalar()
            else:
                return None
            
    @classmethod
    async def find_all_bookings(cls, user_id: int):
        async with async_sessionmaker() as session:
            rooms_alias = aliased(Rooms)
            query = select(
                models.Bookings.id,
                models.Bookings.room_id,
                models.Bookings.user_id,
                models.Bookings.date_from,
                models.Bookings.date_to,
                models.Bookings.price,
                models.Bookings.total_cost,
                models.Bookings.total_days,
                rooms_alias.image_id,
                rooms_alias.name,
                rooms_alias.description,
                rooms_alias.services
            ).where(
                models.Bookings.user_id == user_id
            ).join(
                rooms_alias, rooms_alias.id == models.Bookings.room_id
            )
            result = await session.execute(query)
            return result.mappings().all() 

    @classmethod
    async def delete_booking_user(cls, booking_id: int):
        async with async_sessionmaker() as session:
            booking = select(models.Bookings).where(
                models.Bookings.id == booking_id
            )
            result = await session.execute(booking)
            booking = result.scalar_one_or_none()

            if booking is None:
                raise BookingNotFound
            await session.execute(delete(models.Bookings).where(models.Bookings.id == booking_id))
            await session.commit()