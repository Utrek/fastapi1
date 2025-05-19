import uuid
import config as config
import datetime
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncAttrs
    )
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, DateTime, Float, UUID, ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship


engine = create_async_engine(config.PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):

    @property
    def id_dict(self):
        return {"id": self.id}

class Token(Base):
    __tablename__ = 'token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True,server_default=func.gen_random_uuid()
        )
    creation_token: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
        )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user:  Mapped["User"] = relationship(
        "User",
        lazy="joined",
        back_populates="tokens"
    )

    @property
    def dict(self):
        return {"token": self.token}


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    tokens: Mapped[list[Token]] = relationship(
        "Token",
        lazy="joined",
        back_populates="user"
    )
    adverts: Mapped[list["Advert"]] = relationship(
        "Advert",
        lazy="joined",
        back_populates="user"
    )



class Advert(Base):
    __tablename__ = "advert"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(
        "User",
        lazy="joined",
        back_populates="adverts"
    )
    creation_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
        )

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "description": self.description,
            "user_id": self.user_id,
            "creation_date": self.creation_date.isoformat()

        }


ORM_OBJ = Advert | User | Token
ORM_CLS = type[Advert], type[User], type[Token]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
