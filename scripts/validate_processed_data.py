import csv

PARTS_CSV_PATH = "data/processed/parts_clean.csv"
SUPPLIERS_CSV_PATH = "data/processed/suppliers_clean.csv"
CATEGORIES_CSV_PATH = "data/processed/categories_clean.csv"
PART_SUPPLIERS_CSV_PATH = "data/processed/part_suppliers_clean.csv"

def load_records_from_csv(file_path):
    """
    Loads records from a CSV file into a list of dictionaries.
    """

    records = []

    with open(file_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            records.append(row)

    return records

def validate_unique_field(records, field_name, dataset_name):
    """
    Checks whether a field is unique across a dataset.

    Prints duplicated counts for quick validation feedback.
    """

    seen_values = set()
    duplicate_values = set()

    for record in records:
        value = record[field_name].strip()

        if value in seen_values:
            duplicate_values.add(value)
        
        else:
            seen_values.add(value)

    
    print(f"{dataset_name}: {len(records)} rows loaded")

    if duplicate_values:
        print(f"Duplicate {field_name} values found: {len(duplicate_values)}")
        print(f"First 5 duplicates: {sorted(duplicate_values)[:5]}")

    else:
        print(f"No duplicate {field_name} values found.")

    print()

def validate_part_supplier_relationships(parts, suppliers, part_suppliers):
    """
    Verifies that each part-supplier row references an existing part
    and an existing supplier.

    This is a simple referential integrity check before database work.
    """
    valid_part_numbers = {part["part_number"].strip() for part in parts}
    valid_supplier_codes = {supplier["supplier_code"].strip() for supplier in suppliers}

    missing_parts = []
    missing_suppliers = []

    for record in part_suppliers:
        part_number = record["part_number"].strip()
        supplier_code = record["supplier_code"].strip()

        # Check if parts exist in parts_clean
        if part_number not in valid_part_numbers:
            missing_parts.append(record)

        # Check if suppliers exist in suppliers_clean
        if supplier_code not in valid_supplier_codes:
            missing_suppliers.append(record)

    print(f"Part-supplier rows loaded: {len(part_suppliers)}")

    if missing_parts:
        print(f"Rows with missing part references: {len(missing_parts)}")
        print("First 5 missing part examples:")
        for record in missing_parts[:5]:
            print(record)

    else:
        print("All part references are valid.")

    print()

    if missing_suppliers:
        print(f"Rows with missing supplier references: {len(missing_suppliers)}")
        print("First 5 missing supplier examples:")
        for record in missing_suppliers[:5]:
            print(record)

    else:
        print("All supplier references are valid.")

    print()

if __name__ == "__main__":
    parts = load_records_from_csv(PARTS_CSV_PATH)
    suppliers = load_records_from_csv(SUPPLIERS_CSV_PATH)
    categories = load_records_from_csv(CATEGORIES_CSV_PATH)
    part_suppliers = load_records_from_csv(PART_SUPPLIERS_CSV_PATH)

    print("=== UNIQUE FIELD CHECKS ===")
    print()

    validate_unique_field(parts, "part_number", "Parts")
    validate_unique_field(suppliers, "supplier_code", "Suppliers")
    validate_unique_field(categories, "category_code", "Categories")

    print("=== RELATIONSHIP CHECKS ===")
    print()

    validate_part_supplier_relationships(parts, suppliers, part_suppliers)