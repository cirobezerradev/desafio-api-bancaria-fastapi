from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.accounts import router as account_router
from app.routers.transactions import router as transaction_router

app = FastAPI(
    title='API Bancária',
    )

app.include_router(
    auth_router,
    prefix='/api/v1/auth',
    tags=['auth']
)

app.include_router(
    account_router,
    prefix='/api/v1/accounts',
    tags=['accounts']
)

app.include_router(
    transaction_router,
    prefix='/api/v1/transactions',
    tags=['tansactions']
)
