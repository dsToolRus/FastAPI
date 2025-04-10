from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self,
                      hotel_id,
                      title,
                      low_price,
                      top_price,
                      limit,
                      offset):

        query = select(self.model).filter_by(hotel_id=hotel_id)

        # if hotel_id:
        #     query = query.filter_by(hotel_id=hotel_id)
        if title:
            query = query.filter(self.model.title.like(f"%{title}%"))
        if low_price and top_price:
            query = query.filter(self.model.price.between(low_price, top_price))
        elif low_price:
            query = query.filter(self.model.price >= low_price)
        elif top_price:
            query = query.filter(self.model.price <= top_price)

        query = (query
                 .limit(limit)
                 .offset(offset))

        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [Room.model_validate(item, from_attributes=True) for item in result.scalars().all()]