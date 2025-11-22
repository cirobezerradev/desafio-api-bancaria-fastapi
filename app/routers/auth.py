from fastapi import APIRouter, status

from app.services.security import sign_token
from app.schemas.auth import LoginIn, LoginOut


router = APIRouter()


@router.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_201_CREATED
)
async def login(data: LoginIn) -> LoginOut:
    return sign_token(user_id=data.user_id)
