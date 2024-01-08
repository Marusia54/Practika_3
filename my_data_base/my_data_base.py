from config.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models.userModels import BaseUser
from models.moviesModels import BaseMovies

engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    echo=True,
)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseUser.metadata.create_all)
        await conn.run_sync(BaseMovies.metadata.create_all)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
