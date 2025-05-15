import config as config
import datetime
import sqlalchemy

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, DateTime, Float, func
from sqlalchemy.orm import mapped_column, Mapped


engine = create_async_engine(config.PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    
    @property
    def id_dict(self):
        return {"id":self.id}

class Advert(Base):
    __tablename__ = "Advert"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column (String, index=True)
    description: Mapped[str] = mapped_column (String)
    price: Mapped[float] = mapped_column(Float)
    author: Mapped[str] = mapped_column (String, nullable=False)
    creation_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default= func.now())
    

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "description": self.description,
            "author": self.author,
            "creation_date": self.creation_date.isoformat()
        }
    
ORM_OBJ = Advert
ORM_CLS = type[Advert]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()




