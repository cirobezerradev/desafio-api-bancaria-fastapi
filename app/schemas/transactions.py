from datetime import datetime
from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, Field


class BaseModelOut(BaseModel):
    class Config:
        from_attributes = True


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


class DepositIn(BaseModel):
    account_id: Annotated[
        int,
        Field(
            description='Id da Conta'
        )
    ]
    value: Annotated[
        Decimal,
        Field(
            description='Valor do Depósito'
        )
    ]


class WithdrawIn(BaseModel):
    account_id: Annotated[
        int,
        Field(
            description='Id da conta'
        )
    ]
    value: Annotated[
        Decimal,
        Field(
            description='Valor do Saque'
        )
    ]
