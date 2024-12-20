from fastapi import APIRouter, Depends, Response
from app.users.auth import auth_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserRegister
from app.app_main.excepts import UserAlreadyExists, IncorrectEmailOrPass

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и пользователи"]
)

@router.post("/register")
async def register_user(user_date: SUserRegister):
    existings_user = await UsersDAO.find_one_or_none(email=user_date.email)
    if existings_user:
        raise UserAlreadyExists
    hash_pass = get_password_hash(user_date.password)
    await UsersDAO.add(email=user_date.email, hashed_password=hash_pass)


@router.post("/login")
async def login_user(response: Response, user_date: SUserRegister):
    user = await auth_user(user_date.email, user_date.password)
    if not user:
        raise IncorrectEmailOrPass
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me")
async def read_me(user: Users = Depends(get_current_user)):
    return user