from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Async engine for FastAPI
async_engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

async def init_db():
    async with async_engine.begin() as conn:
        # SQLModel.metadata.create_all(conn) # This doesn't work directly with async engine
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
