from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# Create the SQLAlchemy engine using the database URL from .env
engine = create_engine(
    settings.DATABASE_URL,
    future=True,
)

# Reusable database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def get_db():
    """
    FastAPI dependency for obtaining a database session.
    This will be used later in API routes and services.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()