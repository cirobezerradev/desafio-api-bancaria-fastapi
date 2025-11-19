from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, Field

from app.models import STANDARD_AGENCY
from app.schemas.transactions import TransactionOut


class BaseModelOut(BaseModel):
    class Config:
        from_attributes = True


class AccountIn(BaseModel):
    holder_name: Annotated[
        str,
        Field(
            description='Nome do Titular',
            examples=['João'],
            max_length=30
        )
    ]
    account_number: Annotated[
        str | None,
        Field(
            description='Número da Conta',
            examples=['1'],
            max_length=6,
            default=None
        )
    ]
    agency_code: Annotated[
        str,
        Field(
            description='Codigo da Agência',
            default=STANDARD_AGENCY
        )
    ]
    balance: Annotated[
        Decimal,
        Field(
            description='Saldo da Conta'
        )
    ]


class AccountOut(BaseModelOut):
    id: Annotated[
        int,
        Field(
            description='Id da Conta'
        )
    ]
    holder_name: Annotated[
        str,
        Field(
            description='Nome do Titular',
            max_length=30
        )
    ]
    account_number: Annotated[
        str,
        Field(
            description='Número da Conta',
            max_length=6
        )
    ]
    agency_code: Annotated[
        str,
        Field(
            description='Codigo da Agência',
        )
    ]
    balance: Annotated[
        Decimal,
        Field(
            description='Saldo da Conta Atual'
        )
    ]


class AccountStatementOut(BaseModelOut):
    id: Annotated[
        int,
        Field(
            description='Id da Conta'
        )
    ]
    holder_name: Annotated[
        str,
        Field(
            description='Nome do Titular',
            examples=['João'],
            max_length=30
        )
    ]
    account_number: Annotated[
        str,
        Field(
            description='Número da Conta',
            examples=['1'],
            max_length=6
        )
    ]
    agency_code: Annotated[
        str,
        Field(
            description='Codigo da Agência',
            default=STANDARD_AGENCY
        )
    ]
    balance: Annotated[
        Decimal,
        Field(
            description='Saldo da Conta Atual'
        )
    ]
    transactions: list[TransactionOut]


class AccountUpdate(BaseModelOut):
    holder_name: Annotated[
        str | None,
        Field(
            description='Nome do titular',
            max_length=30,
            default=None
        )
    ]
    # balance: Annotated[
    #     Decimal | None,
    #     Field(
    #         description='Saldo Atual',
    #         default=None
    #     )
    # ]

    class Config:
        extra = 'ignore'
