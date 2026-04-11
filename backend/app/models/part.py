import uuid

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Part(Base):
    __tablename__ = "parts"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Business identifier
    part_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    # Human-readable part description
    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Public-facing price
    public_price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    # Current inventory quantity
    quantity_on_hand: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # Optional category relationship for filtering/browsing
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id"),
        nullable=True,
    )