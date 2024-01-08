from dotenv import load_dotenv
import os


class Settings:
    app_name: str = "New API"
    admin_email: str = "d1225mmo@rb.asu.ru"
    DATABASE_URL_SYNC: str = "postgresql://adminMovie:5806719824@localhost:5432/movies"
    DATABASE_URL_ASYNC: str = "postgresql+asyncpg://adminMovie:5806719824@localhost:5432/movies"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str


load_dotenv()
settings = Settings()

settings.POSTGRES_USER = os.environ.get('POSTGRES_USER')
settings.POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
settings.POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
settings.POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
settings.POSTGRES_DB = os.environ.get('POSTGRES_DB')

settings.DATABASE_URL_SYNC = f"postgresql:" \
                              f"//{settings.POSTGRES_USER}:" \
                              f"{settings.POSTGRES_PASSWORD}" \
                              f"@{settings.POSTGRES_HOST}:" \
                              f"{settings.POSTGRES_PORT}" \
                              f"/{settings.POSTGRES_DB}"

settings.DATABASE_URL_ASYNC = f"postgresql+asyncpg:" \
                              f"//{settings.POSTGRES_USER}:" \
                              f"{settings.POSTGRES_PASSWORD}" \
                              f"@{settings.POSTGRES_HOST}:" \
                              f"{settings.POSTGRES_PORT}" \
                              f"/{settings.POSTGRES_DB}"
