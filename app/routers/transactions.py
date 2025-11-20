from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models import TransactionModel, AccountModel
from app.schemas.transactions import TransactionOut, DepositIn, WithdrawIn


DBSession = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter()


@router.post(
    path='/deposits',
    response_model=TransactionOut,
    status_code=status.HTTP_201_CREATED
)
async def make_deposit(
    deposit_data: DepositIn,
    session: DBSession,
) -> TransactionModel:

    if deposit_data.value <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O valor do depósito deve ser maior que 0"
        )

    stmt = (
        select(AccountModel)
        .where(AccountModel.id == deposit_data.account_id)
        .with_for_update()
    )

    result = await session.execute(stmt)

    account: AccountModel = result.scalar_one_or_none()

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detais=f'Conta com ID {deposit_data.account_id} não encontrada.'
        )

    account.balance += deposit_data.value

    session.add(account)

    transaction = TransactionModel(
        type='DEPÓSITO',
        value=deposit_data.value,
        account_id=deposit_data.account_id
    )

    session.add(transaction)
    try:
        await session.commit()
        await session.refresh(transaction)
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Não foi possível realizar o depósito.\n Erro: {e}'
        )

    return transaction


@router.post(
    path='/withdrawals',
    response_model=TransactionOut,
    status_code=status.HTTP_201_CREATED
)
async def make_withdrawal(
    withdraw_data: WithdrawIn,
    session: DBSession
) -> TransactionOut:

    if withdraw_data.value <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O valor do depósito deve ser maior que 0"
        )

    smtp = (
        select(AccountModel)
        .where(AccountModel.id == withdraw_data.account_id)
        .with_for_update()
    )

    result = await session.execute(smtp)

    account: AccountModel = result.scalar_one_or_none()

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detais=f'Conta com ID {withdraw_data.account_id} não encontrada.'
        )

    if account.balance < withdraw_data.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Saldo Insuficiente'
        )

    account.balance -= withdraw_data.value

    session.add(account)

    transaction = TransactionModel(
        type='SAQUE',
        value=withdraw_data.value,
        account_id=withdraw_data.account_id
    )

    session.add(transaction)

    try:
        await session.commit()
        await session.refresh(account)

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Não foi possível realizar o saque.\n Erro: {e}'
        )

    return transaction


@router.get(
    path='/extrato',
    response_model=list[TransactionOut],
    status_code=status.HTTP_200_OK
)
async def get_statement(
    account_id: int,
    session: DBSession,
    skip: int = 0,
    limit: int = 100
) -> list[TransactionOut]:

    stmt = (
        select(TransactionModel)
        .filter(TransactionModel.account_id == account_id)
        .offset(skip)
        .limit(limit)
    )

    transactions = (await session.scalars(stmt)).all()

    if transactions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Não foi encontrada nenhuma'
            f'trasação na conta ID {account_id}'
        )

    return transactions
