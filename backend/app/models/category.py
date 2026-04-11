import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Category(Base):
    __tablename__ = "categories"

    # Primary key (UUID)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # Short code from cleaned source data, used for imports and matching
    category_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    # Human-readable category name
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    # URL -friendly value for frontend routes
    slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    # Soft-active flag for admin control
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

