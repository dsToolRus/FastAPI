from typing import Optional
from pydantic import BaseModel, Field

class RoomAdd(BaseModel):
    hotel_id: int = Field(description="ID отеля, которому принадлежит номер")
    title: str = Field(description="Класс номера")
    description: Optional[str] = Field(None, description="Описание номера (необязательный)")
    price: int = Field(description="Цена номера")
    quantity: int = Field(description="Количество номеров")

class Room(RoomAdd):
    id: int

class RoomPATCH(BaseModel):
    hotel_id: Optional[int] = Field(None, description="ID отеля, которому принадлежит номер")
    title: Optional[str] = Field(None, description="Класс номера")
    description: Optional[str] = Field(None, description="Описание номера (необязательный)")
    price: Optional[int] = Field(None, description="Цена номера")
    quantity: Optional[int] = Field(None, description="Количество номеров")