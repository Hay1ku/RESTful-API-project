from app.database import async_sessionmaker
from sqlalchemy import select, insert
from pydantic import EmailStr


class BaseReposit:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_sessionmaker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_sessionmaker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_user_password(cls, email: EmailStr):
        async with async_sessionmaker() as session:
            query = select(cls.model).where(cls.model.email == email)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return user.hashed_password
            return None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_sessionmaker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def add(cls, **date):
        async with async_sessionmaker() as session:
            query = insert(cls.model).values(**date)
            await session.execute(query)
            await session.commit()