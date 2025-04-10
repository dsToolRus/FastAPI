from pydantic import BaseModel, Field, EmailStr

class UserRequestAdd(BaseModel):
    email: EmailStr = Field(description="Почта нового пользователя")
    password: str = Field(description="Пароль нового пользователя")

class UserAdd(BaseModel):
    email: EmailStr = Field(description="Почта нового пользователя")
    hashed_password: str = Field(description="Хешированный пароль нового пользователя")

class User(BaseModel):
    id: int
    email: EmailStr = Field(description="Почта нового пользователя")

class UserWithHashedPassword(User):
    hashed_password: str = Field(description="Хешированный пароль нового пользователя")