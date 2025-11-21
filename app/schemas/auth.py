from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field


class LoginIn(BaseModel):
    user_id: Annotated[
        int,
        Field(
            description='Id do Usuário'
        )
    ]


class LoginOut(BaseModel):
    access_token: Annotated[
        str,
        Field(
            description='Token'
        )
    ]


class AccessToken(BaseModel):
    sub: int
    exp: datetime


class JWTToken(BaseModel):
    access_token: AccessToken
