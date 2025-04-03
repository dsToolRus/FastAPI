from typing import Optional
from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str = Field(description="Название курорта")
    name: str = Field(description="Название отеля")

class HotelPATCH(BaseModel):
    title: Optional[str] = Field(None, description="Название курорта")
    name: Optional[str] = Field(None, description="Название отеля")