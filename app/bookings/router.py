from datetime import date
from fastapi import APIRouter, Request, Depends
from app.bookings.reposit import BookingReposit
from app.bookings.schemas import SBooking
from app.tasks.tasks import send_booking_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.app_main.excepts import RoomCannotBooked, NotTokenExpired, IncorrentToken
from pydantic import TypeAdapter, parse_obj_as


router = APIRouter(
    prefix="/bookings",
    tags=['Бронирования'],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):
    if user:
        return await BookingReposit.find_all_bookings(user_id=user.id)
    else:
        raise NotTokenExpired


@router.post("")
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user)
):
    booking = await BookingReposit.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBooked
    
    booking_dict = booking.__dict__ if hasattr(booking, "__dict__") else dict(booking)
    booking_adapter = TypeAdapter(SBooking).validate_python(booking_dict).model_dump()
    send_booking_email.delay(booking_adapter, user.email)
    return booking_adapter


@router.delete("/{booking_id}")
async def delete_booking_user(
    booking_id: int,
    user: Users = Depends(get_current_user)
):
    if user:
        await BookingReposit.delete_booking_user(booking_id=booking_id)
        return {'details': 'Запись удалена'}
    else:
        raise IncorrentToken