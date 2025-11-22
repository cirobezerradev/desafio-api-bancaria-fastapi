from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.accounts import router as account_router
from app.routers.transactions import router as transaction_router
from app.core.settings import api_metadata

app = FastAPI(**api_metadata)

app.include_router(
    auth_router,
    prefix='/auth',
    tags=['auth']
)

app.include_router(
    account_router,
    prefix='/accounts',
    tags=['accounts']
)

app.include_router(
    transaction_router,
    prefix='/transactions',
    tags=['transactions']
)
