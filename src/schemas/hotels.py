from typing import Optional
from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str = Field(description="Название отеля")
    location: str = Field(description="Местоположение")

class HotelPATCH(BaseModel):
    title: Optional[str] = Field(None, description="Название отеля")
    location: Optional[str] = Field(None, description="Местоположение")