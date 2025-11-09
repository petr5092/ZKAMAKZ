from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer
from sqlalchemy.orm import as_declarative
from config import settings


@as_declarative()
class Base:
    id = Column(
        Integer,
        primary_key=True,
    )


engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


