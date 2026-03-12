from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

DATABASE_URL = (
    f"mysql+pymysql://{settings.USER}:{settings.PASSWORD}"
    f"@{settings.HOST}/{settings.DATABASE}"
)

engine = create_engine(
    DATABASE_URL,
    pool_size=settings.POOL_SIZE,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)