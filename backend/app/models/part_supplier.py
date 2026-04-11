"""
PartSupplier model

Represents the relationship between parts and suppliers.

- supplier_cost
- supplier_part_number
- is_preferred

This keeps internal sourcing/cost logic separate from the public-facing
parts table.
"""

import uuid
from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class PartSupplier(Base):
    """
    Junction table between parts and suppliers.

    A part may come from multiple suppliers, and a supplier may provide
    multiple parts. This table stores the supplier-specific relationship.
    """
    __tablename__ = "part_suppliers"

    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Foreign key to Part
    part_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("parts.id"),
        nullable=False,
    )

    # Foreign key to Supplier
    supplier_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("suppliers.id"),
        nullable=False,
    )

    # Cost from this supplier for this part
    supplier_cost: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    # Optional supplier-specific part number
    supplier_part_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # Flag to indicate preferred supplier for this part
    is_preferred: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )