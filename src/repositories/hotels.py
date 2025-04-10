from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self,
                      location,
                      title,
                      limit,
                      offset):
        query = select(self.model)

        if title:
            # query = query.filter_by(title=title)
            query = query.filter(self.model.title.like(f"%{title}%"))
        if location:
            # query = query.filter_by(location=location)
            query = query.filter(self.model.location.like(f"%{location}%"))

        query = (query
                 .limit(limit)
                 .offset(offset))

        result = await self.session.execute(query)
        return [Hotel.model_validate(item, from_attributes=True) for item in result.scalars().all()]


