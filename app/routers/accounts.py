from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException

from app.core.database import get_session
from app.schemas.accounts import AccountOut, AccountIn
from app.models import AccountModel

# Aliás de sessão e dependência
DBSession = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter()


@router.post(
        path='/',
        response_model=AccountOut,
        status_code=status.HTTP_201_CREATED
)
async def create_account(
    account: AccountIn,
    session: DBSession
):
    account = AccountModel(**account.model_dump())
    try:
        session.add(account)
        await session.commit()
        await session.refresh(account)

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Não foi possível criar a conta: {e}'
        )

    return account


@router.get(
    path='/',
    response_model=list[AccountOut],
    status_code=status.HTTP_200_OK
)
async def list_accounts(
    session: DBSession
) -> list[AccountModel]:

    result = await session.scalars(select(AccountModel))
    accounts = result.all()

    return accounts


@router.get(
    path='/{id}',
    response_model=AccountOut,
    status_code=status.HTTP_200_OK
)
async def list_account_by_id(
    id: int,
    session: DBSession
) -> AccountModel:
    
    account = await session.get(AccountModel, id)

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Conta não encontrada com o id: {str(id)}'
        )

    return account
