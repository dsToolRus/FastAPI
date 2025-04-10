from typing import Optional
from pydantic import BaseModel, Field

class HotelAdd(BaseModel):
    title: str = Field(description="Название отеля")
    location: str = Field(description="Местоположение")

class Hotel(HotelAdd):
    id: int

class HotelPATCH(BaseModel):
    title: Optional[str] = Field(None, description="Название отеля")
    location: Optional[str] = Field(None, description="Местоположение")