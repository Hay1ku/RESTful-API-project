from fastapi import HTTPException, status


UserAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует"
)

IncorrectEmailOrPass = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверная почта или пароль"
)


TokenExpired = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Истёк токен"
)

NotTokenExpired = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Нет токена"
)

IncorrentToken = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный формат токена"
)

RoomCannotBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Не осталось свободных номеров"
)

BookingNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Такого booking_id не существует"
)