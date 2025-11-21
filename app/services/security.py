from datetime import datetime, timedelta, timezone
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt
from jwt import ExpiredSignatureError
import os

from app.schemas.auth import JWTToken

load_dotenv()

SECRET = os.getenv('SECRET')
ALGORITHM = os.getenv('STATEMENT')


def sign_token(user_id: int) -> JWTToken:
    payload = {
        'sub': str(user_id),
        'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return {'access_token': token}


def decode_token(token: str) -> JWTToken | None:

    try:
        decoded = jwt.decode(
            token,
            SECRET,
            algorithms=[ALGORITHM],
            options={'verify_sub': False}
        )
        _token = JWTToken.model_validate({'access_token': decoded})

        if not _token.access_token.exp >= datetime.now(timezone.utc):
            return None

        return _token

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Session Expired'
        )

    except Exception as e:
        print(e.__str__)
        return None


def get_current_user(
        token: Annotated[JWTToken, Depends(HTTPBearer())]
) -> dict[str, int]:

    _token = decode_token(token.model_dump()['credentials'])
    print(_token)
    return {'user_id': _token.access_token.sub}


def login_required(
        current_user: Annotated[dict[str, int] | None,
                                Depends(get_current_user)]) -> dict[str, int]:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Access denied'
        )
    print(current_user)
    return current_user
