from fastapi import Query, APIRouter, Body
from typing import Optional
from src.database import async_session_maker
from src.schemas.hotels import HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get('/{hotel_id}', summary="Получение одного отеля по id")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.get('', summary='Получение списка отелей', description="Получение списка отелей по параметрам")
async def get_hotels(
        pagination: PaginationDep,
        title: Optional[str] = Query(None, description="Название курорта"),
        location: Optional[str] = Query(None, description="Местоположение")
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(location=location,
                                                       title=title,
                                                       limit=pagination.per_page,
                                                       offset=pagination.per_page * (pagination.page - 1))


@router.post('', summary='Добавление нового отеля', description="Добавление нового отеля в список отелей")
async def add_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": "example 1", "value": {
        "title": "Солнечный",
        "location": "Калининград"
    }}
})):

    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "Ok", "data": hotel}


@router.delete('/{hotel_id}', summary='Удаление отеля из списка', description="Удаление отеля из списка по его айди")
async def remove_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {'status': 'Ok'}


@router.put('/{hotel_id}', summary='Изменение данных об отеле целиком')
async def put_hotel(hotel_id: int,
                    hotel_data: HotelAdd = Body(openapi_examples=
                    {
                        "1": {"summary": "example 1", "value": {
                                  "title": "Солнечный",
                                  "location": "Калининград"
                                  }
                             }
                    })):

    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {'status': 'Ok'}


@router.patch('/{hotel_id}', summary='Изменение некоторых данных об отеле', description="Изменяет те данные об отеле, которые введены. При отправке пустой строки данные будут стёрты")
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH = Body(openapi_examples={
                  "1": {"summary": "example 1", "value": {
                      "location": "Калининград",
                      "title": "Solnechniy"
                  }},
                  "2": {"summary": "example 2", "value": {
                      "location": "Калининград",
                  }},
                  "3": {"summary": "example 3", "value": {
                      "title": "Солнечный"
                  }},
                  "4": {"summary": "example 4", "value": {
                  }}
              })):

    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()

    return {'status': 'Ok'}