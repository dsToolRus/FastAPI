from fastapi import Query, APIRouter, Body
from src.database import async_session_maker
from src.schemas.rooms import RoomPATCH, RoomAdd
from src.api.dependencies import PaginationDep, RoomFiltersDep
from src.repositories.rooms import RoomsRepository

router = APIRouter(prefix="/hotels", tags=["Комнаты"])

@router.get('/{hotel_id}/rooms',
            summary='Получение списка номеров',
            description="Получение списка номеров в конкретном отеле по фильтрам")
async def get_rooms(
        hotel_id: int,
        pagination: PaginationDep,
        filters: RoomFiltersDep = Query(openapi_examples={
            "1": {
                "summary": "ex 1", "value": {
                    "hotel_id": 1,
                    "title": "Stand"
                }
            },
            "2": {
                "summary": "ex 2", "value": {
                    "hotel_id": 1,
                    "low_price": 1000,
                    "top_price": 5000
                }
            },
            "3": {
                "summary": "ex 3", "value": {
                    "low_price": 2000,
                    "top_price": 4000
                }
            },
            "4": {
                "summary": "ex 4", "value": {
                    "title": "lux",
                    "top_price": 5000
                }
            },
            "5": {
                "summary": "ex 5", "value": {
                    "low_price": 2000
                }
            },
            "6": {
                "summary": "ex 6", "value": {
                    "hotel_id": 3
                }
            }
        })
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id,
                                                      title=filters.title,
                                                      low_price=filters.low_price,
                                                      top_price=filters.top_price,
                                                      limit=pagination.per_page,
                                                      offset=pagination.per_page * (pagination.page - 1))


@router.get('/{hotel_id}/rooms/{room_id}',
            summary="Получение одного номера",
            description="Получение одного номера по id отеля и номера")
async def get_room(
        hotel_id: int,
        room_id: int
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id,
                                                              id=room_id)


@router.post('/add_room',
             summary='Добавление номера в отель',
             description="Добавление нового номера в конкретный отель")
async def add_room(
        room_data: RoomAdd = Body(openapi_examples={
            "1": {
                "summary": "room 1", "value": {
                    "hotel_id": 1,
                    "title": "Standart",
                    "description": "Самый обычный номер",
                    "price": 1500,
                    "quantity": 20
                }
            },
            "2": {
                "summary": "room 2", "value": {
                    "hotel_id": 2,
                    "title": "Delux",
                    "price": 2500,
                    "quantity": 15
                }
            },
            "3": {
                "summary": "room 3", "value": {
                    "hotel_id": 2,
                    "title": "Ultra",
                    "description": "Шикарный номер, всё включено",
                    "price": 5000,
                    "quantity": 12
                }
            }
        })
):
    async with async_session_maker() as session:
        added_room = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "Ok", "data": added_room}


@router.delete('/{hotel_id}/rooms/{room_id}',
               summary='Удаление номера из отеля',
               description="Удаление номера из отеля по id номера и отеля")
async def remove_room(
        hotel_id: int,
        room_id: int
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id,
                                              id=room_id)
        await session.commit()

    return {'status': 'Ok'}


@router.put('/{hotel_id}/rooms/{room_id}',
            summary='Изменение данных о номере',
            description="Изменение данных о номере целиком по id номера и отеля")
async def put_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAdd = Body(openapi_examples={
            "1": {
                "summary": "example 1", "value": {
                    "hotel_id": 1,
                    "title": "Delux",
                    "description": "Номер превосходного качества!",
                    "price": 6500,
                    "quantity": 6
                }
            },
            "2": {
                "summary": "example 2", "value": {
                    "hotel_id": 2,
                    "title": "Standart",
                    "price": 2700,
                    "quantity": 42
                }
            }
        })
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
        await session.commit()

    return {'status': 'Ok'}


@router.patch('/{hotel_id}/rooms/{room_id}',
              summary='Изменение некоторых данных о номере',
              description="Изменяет те данные о номере, которые введены. При отправке пустой строки данные будут стёрты")
async def patch_room(
        room_id: int,
        room_data: RoomPATCH = Body(openapi_examples={
            "1": {
                "summary": "example 1", "value": {
                    "hotel_id": 1,
                    "title": "Delux",
                    "description": "Номер превосходного качества!",
                    "price": 6500,
                    "quantity": 6
                }
            },
            "2": {
                "summary": "example 2", "value": {
                    "hotel_id": 2,
                    "title": "Standart",
                    "price": 2700,
                    "quantity": 42
                }
            },
            "3": {
                "summary": "example 3", "value": {
                    "hotel_id": 2,
                    "title": "Standart"
                }
            },
            "4": {
                "summary": "example 4", "value": {
                    "hotel_id": 3,
                    "price": 2700,
                    "quantity": 5
                }
            },
            "5": {
                "summary": "example 5", "value": {
                    "hotel_id": 1,
                    "title": "Delux",
                    "price": 2700
                }
            }
        })
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()

    return {'status': 'Ok'}