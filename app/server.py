from fastapi import FastAPI
from shema import( 
    CreateAdvertRequest, CreateAdvertResponse, 
    UpdateAdvertRequest, UpdateAdvertResponse, 
    GetAdvertResponse,
    SeachAdvertResponse,
    DeleteAdvertResponse
    ) 

import crud
from lifespan import lifespan    
from models import Session
import models
from depandancy import SessionDependency
from sqlalchemy import select
from constants import SUCCESS_RESPONSE
 
app = FastAPI(
    title = "purchase_sale",
    terms_of_service = "be honest",
    description= "purchase and sale service",
    lifespan= lifespan
)

@app.post("/api/v1/advert", tags = ["advert"], response_model=CreateAdvertResponse)
async def create_advert (advert: CreateAdvertRequest, session:SessionDependency):
    advert_dict = advert.model_dump(exclude_unset=True)
    advert_orm_obj = models.Advert(**advert_dict)
    await crud.add_item(session, advert_orm_obj)
    return advert_orm_obj.id_dict

@app.get("/api/v1/advert/{advert_id}", tags = ["advert"], response_model=GetAdvertResponse)
async def get_advert(advert_id: int, session:SessionDependency):
    advert_orm_obj =await crud.get_item_by_id(session, models.Advert, advert_id)
    return advert_orm_obj.dict

@app.get("/api/v1/advert/", tags = ["advert"], response_model=SeachAdvertResponse )
async def seach_advert(session: SessionDependency, title: str):
    query = select(models.Advert).where( models.Advert.title == title).limit(10000)
    adverts = await session.scalars(query)
    return {"results":[advert.dict for advert in adverts]}

@app.patch("/api/v1/advert/{advert_id}", tags = ["advert"], response_model=UpdateAdvertResponse)
async def update_advert(advert_id: int, advert_data:UpdateAdvertRequest, session:SessionDependency):
    advert_dict = advert_data.model_dump(exclude_unset=True)
    advert_orm_obj =await crud.get_item_by_id(session, models.Advert, advert_id)

    for field, value in advert_dict.items():
        setattr(advert_orm_obj, field, value)
    await crud.add_item(session, advert_orm_obj)
    return SUCCESS_RESPONSE

@app.delete("/api/v1/advert/{advert_id}", tags = ["advert"], response_model=DeleteAdvertResponse)
async def delete_advert(advert_id: int, session: SessionDependency):
    advert_orm_obj = await crud.get_item_by_id(session, models.Advert, advert_id)
    await crud.delete_item(session, advert_orm_obj)
    return SUCCESS_RESPONSE




