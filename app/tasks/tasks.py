from pydantic import EmailStr
from app.tasks.celery import celery
from PIL import Image
from pathlib import Path
from app.tasks.email_templates import create_booking_message
import smtplib
from app.app_main.config import settings


@celery.task
def process_pic(
    path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_res_1000_500 = im.resize((1000, 500))
    im_res_200_100 = im.resize((200, 100))
    im_res_1000_500.save(f"app/static/images/res_1000_500{im_path.name}")
    im_res_200_100.save(f"app/static/images/res_200_100{im_path.name}")


@celery.task
def send_booking_email(
    booking: dict,
    email_to: EmailStr,
):
    content = create_booking_message(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(content)