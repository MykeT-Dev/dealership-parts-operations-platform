from sqlalchemy import Column, String, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base import Base

class Part(Base):
    __tablename__ = "parts"

    # Primary key (UUID)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Business identifier
    part_number = Column(String, unique=True, nullable=False)

    # Description of the part
    description = Column(String, nullable=True)

    # Public-facing price of the part
    public_price = Column(Numeric(10, 2), nullable=False)

    # Inventory count
    quantity_on_hand = Column(Integer, default=0, nullable=False)