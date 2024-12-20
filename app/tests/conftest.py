from datetime import datetime
import json
import pytest_asyncio
from sqlalchemy import insert
from app.database import Base, async_sessionmaker, engine
from app.app_main.config import settings

from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users
from app.bookings.models import Bookings

from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from app.app_main.main import app as fast_app


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r", encoding="utf-8") as file:
            return json.load(file)
    hotels = open_mock_json('hotels')
    rooms = open_mock_json('rooms')
    users = open_mock_json('users')
    bookings = open_mock_json('bookings')

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_sessionmaker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_user = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_user)
        await session.execute(add_bookings)

        await session.commit()


@pytest_asyncio.fixture(scope="function")
async def ac():
    transport = ASGITransport(fast_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

# @pytest_asyncio.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
