from src.database import BaseOrm
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from typing import Optional

class RoomsOrm(BaseOrm):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[str] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]]
    price: Mapped[int]
    quantity: Mapped[int]