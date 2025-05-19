from pydantic import BaseModel
from typing import Literal
import datetime


class IdResponse(BaseModel):
    id: int


class SuccessResponse(BaseModel):
    status: Literal['success']


class CreateAdvertRequest(BaseModel):
    title: str
    description: str
    price: float
    author: str


class CreateAdvertResponse(IdResponse):
    pass


class UpdateAdvertRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None


class UpdateAdvertResponse(SuccessResponse):
    pass


class GetAdvertResponse(BaseModel):
    id: int
    title: str
    price: float
    description: str
    creation_date: datetime.datetime
    author: str


class SeachAdvertResponse(BaseModel):
    results: list[GetAdvertResponse]


class DeleteAdvertResponse(SuccessResponse):
    pass
