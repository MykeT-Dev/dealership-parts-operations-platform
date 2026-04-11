"""
Supplier model

Represents a vendor or distributor that provides parts.
This is intentionally simple for MVP, but structured to support
supplier-specific cost logic later (via part_suppliers table).
"""

import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Supplier(Base):
    """
    Supplier entity

    Each supplier represents a source where parts can be purchased.
    This table does NOT store cost per part — that belongs in the
    part_suppliers relationship table.
    """
    __tablename__ = "suppliers"

    # Primary key (UUID)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # Short code from source data
    supplier_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    # Display name
    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # Soft-delete / active flag for admin control
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )