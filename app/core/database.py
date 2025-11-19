from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker)


DATABASE_URL = "sqlite+aiosqlite:///./app/banco.db"

engine = create_async_engine(DATABASE_URL)

session_async = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)


async def get_session():
    async with session_async() as session:
        yield session
