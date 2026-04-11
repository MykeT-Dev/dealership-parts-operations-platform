"""
Pydantic schemas for part API responses.

These schemas define what the public API is allowed to return.
They intentionally exclude internal-only fields such as supplier cost.
"""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class PartListItem(BaseModel):
    """
    Public-safe representation of a part for list endpoints.
    """

    id: UUID
    part_number: str
    description: str
    public_price: Decimal
    stock_status: str
    category_name: str | None = None
    category_code: str | None = None

class PartDetail(BaseModel):
    """
    Public-safe representation of a single part.
    """

    id: UUID
    part_number: str
    description: str
    public_price: Decimal
    stock_status: str
    category_name: str | None = None
    category_code: str | None = None

class PartListResponse(BaseModel):
    """
    Response schema for the parts list endpoint.
    """

    limit: int
    offset: int
    count: int
    items: list[PartListItem]