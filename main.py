from fastapi import FastAPI, Query, Body
import uvicorn
from typing import Optional

app = FastAPI()

hotels = [
    {"id": 1, "title": "Сочи", "name": "Южный"},
    {"id": 2, "title": "Анапа", "name": "Звезда"},
    {"id": 3, "title": "Абхазия", "name": "Пич"}
]

@app.get('/hotels')
def get_hotels(title: Optional[str] = Query(None, description="Название курорта")):
    hotels_ = []
    for hotel in hotels:
        if title and hotel["title"] != title:
            continue

        hotels_.append(hotel)
    return hotels_

@app.delete('/hotels/{hotel_id}')
def remove_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {'status': 'Ok'}

@app.post('/hotels')
def add_hotel(title: str = Body(description="Название курорта"),
              name: str = Body(description="Название отеля")):

    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
    return {'status': 'Ok'}

@app.put('/hotels/{hotel_id}')
def put_hotel(hotel_id: int,
              title: str = Body(description="Название курорта"),
              name: str = Body(description="Название отеля")):

    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name

            return {'status': 'Ok'}


@app.patch('/hotels/{hotel_id}')
def patch_hotel(
        hotel_id: int,
        title: Optional[str] = Body(None, description="Название курорта"),
        name: Optional[str] = Body(None, description="Название отеля")):

    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name

            return {'status': 'Ok'}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)