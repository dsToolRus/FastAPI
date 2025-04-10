from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, Annotated
from src.services.auth import AuthService

class PaginationParams(BaseModel):
    page: Annotated[Optional[int], Query(1, description="Номер страницы", gt=0)]
    per_page: Annotated[Optional[int], Query(5, description="Число объектов на странице", gt=0, lt=21)]

PaginationDep = Annotated[PaginationParams, Depends()]



def get_token(request: Request) -> str:
    token = request.cookies.get('access_token', None)
    if not token:
        raise HTTPException(status_code=401, detail="Incorrect token")

    return token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    decoded_token = AuthService().decode_token(token)

    return decoded_token.get("user_id", None)

UserIdDep = Annotated[int, Depends(get_current_user_id)]



class RoomFilters(BaseModel):
    # hotel_id: Annotated[Optional[int], Query(None, description="ID отеля, которому принадлежит номер")]
    title: Annotated[Optional[str], Query(None, description="Класс номера")]
    low_price: Annotated[Optional[int], Query(None, description="Нижний предел стоимости номера")]
    top_price: Annotated[Optional[int], Query(None, description="Верхний предел стоимости номера")]

RoomFiltersDep = Annotated[RoomFilters, Depends()]