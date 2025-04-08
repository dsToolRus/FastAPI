from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        statement = (insert(self.model)
                     .values(**data.model_dump())
                     .returning(self.model))
        result = await self.session.execute(statement)
        return result.scalars().one()

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filters) -> None:

        statement = (update(self.model)
                     .filter_by(**filters)
                     .values(**data.model_dump(exclude_unset=exclude_unset)))
        print(statement.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(statement)

    async def delete(self, **filters):
        statement = delete(self.model).filter_by(**filters)
        print(statement.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(statement)