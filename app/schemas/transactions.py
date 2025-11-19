from datetime import datetime
from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, Field


class BaseModelOut(BaseModel):
    class Config:
        from_attributes = True


class TransactionIn(BaseModel):
    type: Annotated[
        str,
        Field(
            description='Tipo da Transação',
            max_length=15
        )
    ]
    value: Annotated[
        Decimal,
        Field(
            description='Valor da Transação'
        )
    ]
    account_id: Annotated[
        int,
        Field(
            description='Id da Conta'
        )
    ]
    created_at: Annotated[
        datetime,
        Field(
            description='Data da Transação'
        )
    ]


class TransactionOut(BaseModelOut):
    id: Annotated[
        int,
        Field(
            description='Id da Transação'
        )
    ]
    type: Annotated[
        str,
        Field(
            description='Tipo da Transação',
            max_length=15
        )
    ]
    value: Annotated[
        Decimal,
        Field(
            description='Valor da Transação'
        )
    ]
    account_id: Annotated[
        int,
        Field(
            description='Id da Conta'
        )
    ]
    created_at: Annotated[
        datetime,
        Field(
            description='Data da Transação'
        )
    ]
