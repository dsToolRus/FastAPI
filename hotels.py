from fastapi import Query, APIRouter, Body
from typing import Optional
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Сочи", "name": "Южный"},
    {"id": 2, "title": "Анапа", "name": "Звезда"},
    {"id": 3, "title": "Абхазия", "name": "Peach"},
    {"id": 4, "title": "Анапа", "name": "Пляжный"},
    {"id": 5, "title": "Сочи", "name": "Взморье"},
    {"id": 6, "title": "Анапа", "name": "Барабулька"},
    {"id": 7, "title": "Абхазия", "name": "Песочный"},
    {"id": 8, "title": "Сочи", "name": "Закат"},
    {"id": 9, "title": "Сочи", "name": "Лазурь"},
    {"id": 10, "title": "Анапа", "name": "Первый"},
    {"id": 11, "title": "Абхазия", "name": "Asure"}
]


@router.get('', summary='Получение списка отелей', description="Получение списка отелей по параметру title, либо всех отелей, если title не задан")
def get_hotels(
        id: Optional[int] = Query(None, description="Айдишник"),
        title: Optional[str] = Query(None, description="Название курорта"),
        page: Optional[int] = Query(1, description="Число отелей на странице"),
        per_page: Optional[int] = Query(3, description="Число отелей на странице")):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue

        hotels_.append(hotel)
    return hotels_[(page - 1) * per_page:page * per_page]


@router.post('', summary='Добавление нового отеля', description="Добавление нового отеля в список отелей")
def add_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "example 1", "value": {
        "title": "Калининград",
        "name": "Солнечный"
    }}
})):

    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {'status': 'Ok'}


@router.delete('/{hotel_id}', summary='Удаление отеля из списка', description="Удаление отеля из списка по его айди")
def remove_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {'status': 'Ok'}


@router.put('/{hotel_id}', summary='Изменение данных об отеле целиком')
def put_hotel(hotel_id: int,
              hotel_data: Hotel = Body(openapi_examples={
                  "1": {"summary": "example 1", "value": {
                      "title": "Калининград",
                      "name": "Солнечный"
                  }}
              })):

    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name

            return {'status': 'Ok'}


@router.patch('/{hotel_id}', summary='Изменение некоторых данных об отеле', description="Изменяет те данные об отеле, которые введены. При отправке пустой строки данные будут стёрты")
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH = Body(openapi_examples={
                  "1": {"summary": "example 1", "value": {
                      "title": "Калининград",
                      "name": "Solnechniy"
                  }},
                  "2": {"summary": "example 2", "value": {
                      "title": "Калининград",
                  }},
                  "3": {"summary": "example 3", "value": {
                      "name": "Солнечный"
                  }},
                  "4": {"summary": "example 4", "value": {
                  }}
              })):

    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name

            return {'status': 'Ok'}