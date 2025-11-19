from fastapi import FastAPI
from app.routers.accounts import router as account_router

app = FastAPI(
    title='API Bancária',
    )

app.include_router(
    account_router,
    prefix='/api/v1/accounts',
    tags=['accounts']
)
