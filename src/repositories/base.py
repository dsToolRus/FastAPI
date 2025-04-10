from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(item, from_attributes=True) for item in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)

        print(query.compile(compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        item = result.scalars().one_or_none()
        if item is None:
            return None
        return self.schema.model_validate(item, from_attributes=True)

    async def add(self, data: BaseModel):
        statement = (insert(self.model)
                     .values(**data.model_dump())
                     .returning(self.model))

        print(statement.compile(compile_kwargs={"literal_binds": True}))

        item = await self.session.execute(statement)
        return self.schema.model_validate(item.scalars().one(), from_attributes=True)

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
