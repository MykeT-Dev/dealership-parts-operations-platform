"""
Seed/import script for the Dealership Parts Operations Platform.

Loads cleaned CSV data into PostgreSQL in the correct dependency order:

1. categories
2. suppliers
3. parts
4. part_suppliers

This script is intended for local development while building the MVP.
"""

import csv
from decimal import Decimal
from pathlib import Path

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.category import Category
from app.models.part import Part
from app.models.part_supplier import PartSupplier
from app.models.supplier import Supplier


# Base path for processed CSV files
BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

CATEGORIES_CSV = PROCESSED_DATA_DIR / "categories_clean.csv"
SUPPLIERS_CSV = PROCESSED_DATA_DIR / "suppliers_clean.csv"
PARTS_CSV = PROCESSED_DATA_DIR / "parts_clean.csv"
PART_SUPPLIERS_CSV = PROCESSED_DATA_DIR / "part_suppliers_clean.csv"


def load_csv_rows(file_path: Path) -> list[dict]:
    """Load a CSV file into a list of dictionaries."""
    with open(file_path, newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def import_categories(db) -> None:
    """
    Import categories first.

    Categories are matched by category_code, since that is the stable key
    from the cleaned source data.
    """
    rows = load_csv_rows(CATEGORIES_CSV)

    for row in rows:
        existing_category = db.scalar(
            select(Category).where(Category.category_code == row["category_code"])
        )

        if existing_category:
            continue

        category = Category(
            category_code=row["category_code"],
            name=row["name"],
            slug=row["name"].strip().lower().replace(" ", "-"),
            is_active=True,
        )
        db.add(category)

    db.commit()
    print(f"Imported categories from {CATEGORIES_CSV.name}")


def import_suppliers(db) -> None:
    """
    Import suppliers next.

    Suppliers are matched by supplier_code from the cleaned dataset.
    """
    rows = load_csv_rows(SUPPLIERS_CSV)

    for row in rows:
        existing_supplier = db.scalar(
            select(Supplier).where(Supplier.supplier_code == row["supplier_code"])
        )

        if existing_supplier:
            continue

        supplier = Supplier(
            supplier_code=row["supplier_code"],
            display_name=row["display_name"],
            is_active=True,
        )
        db.add(supplier)

    db.commit()
    print(f"Imported suppliers from {SUPPLIERS_CSV.name}")


def import_parts(db) -> None:
    """
    Import parts after categories.

    The CSV stores category_code, but the database stores category_id.
    So we look up the category row first, then assign its UUID.
    """
    rows = load_csv_rows(PARTS_CSV)

    for row in rows:
        existing_part = db.scalar(
            select(Part).where(Part.part_number == row["part_number"])
        )

        if existing_part:
            continue

        category = db.scalar(
            select(Category).where(Category.category_code == row["category_code"])
        )

        part = Part(
            part_number=row["part_number"],
            description=row["description"],
            public_price=Decimal(row["public_price"]),
            quantity_on_hand=int(float(row["quantity"])),
            category_id=category.id if category else None,
        )
        db.add(part)

    db.commit()
    print(f"Imported parts from {PARTS_CSV.name}")


def import_part_suppliers(db) -> None:
    """
    Import part-supplier relationships last.

    This table depends on both parts and suppliers already existing.
    """
    rows = load_csv_rows(PART_SUPPLIERS_CSV)

    for row in rows:
        part = db.scalar(
            select(Part).where(Part.part_number == row["part_number"])
        )
        supplier = db.scalar(
            select(Supplier).where(Supplier.supplier_code == row["supplier_code"])
        )

        # Skip rows if the parent records were not found
        if not part or not supplier:
            continue

        existing_relationship = db.scalar(
            select(PartSupplier).where(
                PartSupplier.part_id == part.id,
                PartSupplier.supplier_id == supplier.id,
            )
        )

        if existing_relationship:
            continue

        relationship = PartSupplier(
            part_id=part.id,
            supplier_id=supplier.id,
            supplier_part_number=row["supplier_part_number"] or None,
            supplier_cost=Decimal(row["supplier_cost"]),
            is_preferred=row["is_preferred"].strip().lower() == "true",
        )
        db.add(relationship)

    db.commit()
    print(f"Imported part-supplier relationships from {PART_SUPPLIERS_CSV.name}")


def main() -> None:
    """Run the full import process in dependency order."""
    db = SessionLocal()

    try:
        import_categories(db)
        import_suppliers(db)
        import_parts(db)
        import_part_suppliers(db)
        print("Seed import complete.")
    finally:
        db.close()


if __name__ == "__main__":
    main()