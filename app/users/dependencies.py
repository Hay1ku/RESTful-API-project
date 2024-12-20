from fastapi import Request, HTTPException, Depends, status
from jose import jwt, JWTError
from app.app_main.config import settings
from datetime import datetime, timezone
from app.users.dao import UsersDAO
from app.app_main.excepts import TokenExpired, NotTokenExpired, IncorrentToken


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise NotTokenExpired
    return token



async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrentToken
    
    expire: str = payload.get("exp")
    if not expire or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpired
    
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return user
