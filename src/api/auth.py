from fastapi import APIRouter, HTTPException, Response, Request

from src.api.dependencies import UserIdDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register")
async def register_user(data: UserRequestAdd):
    hashed_password = AuthService().hash_password(data.password)
    hashed_users_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        is_presented = await UsersRepository(session).get_one_or_none(email=data.email)
        if is_presented:
            return {"status": "Not Ok"}
        else:
            user = await UsersRepository(session).add(hashed_users_data)
            await session.commit()

    return {"status": "Ok", "user": user}

@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="User not registered")
        else:
            if not AuthService().verify_password(data.password, user.hashed_password):
                raise HTTPException(status_code=401, detail="Incorrect email or password")
            else:
                access_token = AuthService().create_access_token({"user_id": user.id})
                response.set_cookie("access_token", access_token)
                return {"access_token": access_token}

@router.get("/me")
async def get_me(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user

@router.get("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "Ok"}