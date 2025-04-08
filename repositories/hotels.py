from sqlalchemy import select

from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm

class HotelsRepository(BaseRepository):
    model = HotelsOrm

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
        return result.scalars().all()


