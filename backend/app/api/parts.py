"""
Public parts API routes.

These routes expose public-safe inventory data only.
They do not include internal supplier cost or margin data.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.category import Category
from app.models.part import Part
from app.schemas.part import PartDetail, PartListItem
from app.schemas.part import PartListItem, PartListResponse


router = APIRouter(prefix="/parts", tags=["Parts"])

def get_public_stock_status(quantity_on_hand: int) -> str:
    """
    Convert internal inventory quantity to a public stock status.
    """
    if quantity_on_hand <=0:
        return "Out of Stock"
    if quantity_on_hand <= 5:
        return "Low Stock"
    return "In Stock"


@router.get("", response_model=PartListResponse)
def list_parts(
    search: str | None = Query(
        default=None,
        description="Search by part number or description.",
    ),
    part_number: str | None = Query(
        default=None,
        description="Filter by exact part number.",
    ),
    category: str | None = Query(
        default=None,
        description="Filter by category code, such as ACC.",
    ),
    limit: int = Query(
        default=25,
        ge=1,
        le=100,
        description="Maximum number of parts to return.",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of parts to skip before returning results.",
    ),
    in_stock: bool | None = Query(
        default=None,
        description="If true, only return parts that are currently in stock.",
    ),

    db: Session = Depends(get_db),
):
    """
    Return a public-safe list of parts.

    Optional query params:
    - search: filters by part number or description
    - category: filters by category code
    - limit: maximum number of results to return
    - offset: number of rows to skip
    - in_stock: if true, only return parts currently in stock
    - part_number: exact part number lookup (takes priority over search)

    This query joins categories so the frontend can show category
    labels without exposing any internal supplier data.
    """
    statement = (
        select(
            Part.id,
            Part.part_number,
            Part.description,
            Part.public_price,
            Part.quantity_on_hand,
            Category.name.label("category_name"),
            Category.category_code.label("category_code"),
        )
        .outerjoin(Category, Part.category_id == Category.id)
    )

    # Apply exact part number to lookup if provided (takes priority over search)
    if part_number:
        statement = statement.where(
            Part.part_number == part_number.strip()
        )
    else:

        # Apply search filter if provided
        if search:
            search_term = f"%{search.strip()}%"
            statement = statement.where(
                or_(
                    Part.part_number.ilike(search_term),
                    Part.description.ilike(search_term),
                )
            )

        # Apply category filter if provided
        if category:
            statement = statement.where(
                Category.category_code.ilike(category.strip())
            )

        # Apply in-stock filter if requested
        if in_stock is True:
            statement = statement.where(Part.quantity_on_hand > 0)

    # Apply stable ordering before pagination
    statement = (
        statement
        .order_by(Part.part_number)
        .offset(offset)
        .limit(limit)
    )

    rows = db.execute(statement).all()

    items = [
        PartListItem(
            id=row.id,
            part_number=row.part_number,
            description=row.description,
            public_price=row.public_price,
            stock_status=get_public_stock_status(row.quantity_on_hand),
            category_name=row.category_name,
            category_code=row.category_code,
        )
        for row in rows
    ]

    return PartListResponse(
        limit=limit,
        offset=offset,
        count=len(items),
        items=items,
    )



@router.get("/{part_id}", response_model=PartDetail)
def get_part(part_id: UUID, db: Session = Depends(get_db)):
    """
    Return a single public-safe part by ID.

    Raises:
        404: If the part does not exist.
    """
    statement = (
        select(
            Part.id,
            Part.part_number,
            Part.description,
            Part.public_price,
            Part.quantity_on_hand,
            Category.name.label("category_name"),
            Category.category_code.label("category_code"),
        )
        .outerjoin(Category, Part.category_id == Category.id)
        .where(Part.id == part_id)
    )

    row = db.execute(statement).first()

    if row is None:
        raise HTTPException(status_code=404, detail="Part not found")

    return PartDetail(
        id=row.id,
        part_number=row.part_number,
        description=row.description,
        public_price=row.public_price,
        stock_status=get_public_stock_status(row.quantity_on_hand),
        category_name=row.category_name,
        category_code=row.category_code,
    )