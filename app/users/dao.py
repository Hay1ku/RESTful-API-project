from app.reposit.base import BaseReposit
from app.users.models import Users


class UsersDAO(BaseReposit):
    model = Users