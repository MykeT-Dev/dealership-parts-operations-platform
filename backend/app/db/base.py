from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass

# Import models so Alembic can detect them
from app.models.part import Part

# Import Categories
from app.models.category import Category