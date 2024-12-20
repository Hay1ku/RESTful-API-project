from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.app_main.config import settings


if settings.MODE == "TEST":
    DATABESE_URL = settings.DATABASE_URL_TEST
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABESE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}


engine = create_async_engine(DATABESE_URL, **DATABASE_PARAMS)

async_sessionmaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
