from app.bookings.reposit import BookingReposit
import pytest
from datetime import datetime


@pytest.mark.asyncio
async def test_add_and_get_booking():
    new_booking = await BookingReposit.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d").date(),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d").date()
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingReposit.find_by_id(new_booking.id)

    assert new_booking is not None