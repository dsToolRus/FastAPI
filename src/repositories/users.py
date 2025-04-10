from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User
from sqlalchemy import select
from src.schemas.users import UserWithHashedPassword
from pydantic import EmailStr

class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        item = result.scalars().one()
        return UserWithHashedPassword.model_validate(item, from_attributes=True)