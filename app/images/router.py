from fastapi import APIRouter, UploadFile
import shutil
from app.tasks.tasks import process_pic


router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"]
)

@router.post("/hotels")
async def add_hotel_images(name: int, file: UploadFile):
    img_path = f"app/static/images/{name}.webp"
    with open(img_path, "wb+") as file_obj:
        shutil.copyfileobj(file.file, file_obj)
    process_pic.delay(img_path)