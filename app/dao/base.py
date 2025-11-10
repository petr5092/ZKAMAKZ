from sqlalchemy import select, insert
from database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id):
        async with async_session_maker() as session:
            queary = select(cls.model).filter_by(id=model_id)
            result = await session.execute(queary)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_by_fil(cls, **filter_by):
        async with async_session_maker() as session:
            queary = select(cls.model).filter_by(**filter_by)
            result = await session.execute(queary)
            return result.scalar_one_or_none()
        
    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:
            queary = select(cls.model).filter_by(**filter_by)
            result = await session.execute(queary)
            return result.scalars().all()
        
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            queary = insert(cls.model).values(**data)
            await session.execute(queary)
            await session.commit()