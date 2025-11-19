from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException

from app.core.database import get_session
from app.schemas.accounts import AccountOut, AccountIn, AccountUpdate
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


@router.patch(
    path='/update/{id}',
    response_model=AccountOut,
    status_code=status.HTTP_200_OK
)
async def update_account(
    id: int,
    account_data: AccountUpdate,
    session: DBSession
) -> AccountModel:

    account = await session.scalar(
        select(AccountModel).where(AccountModel.id == id)
    )

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Com com ID: {id} não encontrada.'
        )

    update_data = account_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(account, key, value)

    try:
        session.add(account)
        await session.commit()
        await session.refresh(account)

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Não foi possível atualizar a conta: {e}'
        )
 
    return account


@router.delete(
    path='/delete/{id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def detele_account(
    id: int,
    session: DBSession
):
    account = await session.scalar(
        select(AccountModel).where(AccountModel.id == id)
    )

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Não foi encontrada a conta com id: {str(id)}'
        )
    try:
        await session.delete(account)
        await session.commit()

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Não foi possível deletar a conta, erro:{e}'
        )
