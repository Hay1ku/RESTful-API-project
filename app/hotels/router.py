from fastapi import APIRouter, HTTPException, Response
from app.hotels.dao import HotelsDAO
from datetime import date
from fastapi_cache.decorator import cache
from app.hotels.schemas import SHotels
from typing import List

router = APIRouter(
    prefix="/hotels",
    tags=["Отели и комнаты"]
)


@router.get("/{location}")
@cache(expire=30)
async def get_hotels(
    location: str,
    date_from: date,
    date_to: date
) -> List[SHotels]:
    try:
        # await asyncio.sleep(3)
        hotels = await HotelsDAO.find_all_hotels(date_from, date_to)   
        # Фильтрация по местоположению
        hotels_filtered = [hotel for hotel in hotels if location.lower() in hotel["location"].lower()]

        if not hotels_filtered:
            raise HTTPException(status_code=404, detail="Отели не найдены")
        return hotels_filtered

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")
    

@router.get("/{hotel_id}/rooms")
async def get_hotels_rooms(
    hotel_id: int,
    date_from: date,
    date_to: date,
):
    rooms = await HotelsDAO.find_all_hotels_rooms(
        hotel_id, 
        date_from,
        date_to)
    return rooms