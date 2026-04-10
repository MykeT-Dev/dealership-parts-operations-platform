import csv

INPUT_CSV_PATH = "data/processed/parts_inventory_clean.csv"
OUTPUT_CSV_PATH = "data/processed/part_suppliers_clean.csv"

def load_records_from_csv(file_path):
    """
    Loads records from the cleaned CSV file into a list of dictionaries.
    """

    records = []

    with open(file_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            records.append(row)

    return records

def extract_part_suppliers(records):
    """
    Extracts a normalized part-supplier dataset from cleaned inventory records.
    
    Each row represents a supplier-specific relationship for a part.
    this keeps supplier cost separate from the parts dataset, which
    better matches the normalized database design.

    - Use part_number + supplier_code as the unique relationship key
    - Keep the first occurrence of each unique part/supplier pair
    - Use part_number as a placeholder supplier_part_number
    - Mark each relationship as preferred for now
    """

    unique_part_suppliers = {}

    for record in records:
        # Pull the two fields that define the relationship
        part_number = record["part_number"].strip()
        supplier_code = record["supplier_code"].strip()

        # Skip incomlete rows
        if not part_number or not supplier_code:
            continue

        # Use a tuple as the unique key for each part/supplier relationship
        relationship_key = (part_number, supplier_code)

        # Keep only the first occurrence for MVP
        if relationship_key not in unique_part_suppliers:
            unique_part_suppliers[relationship_key] = {
                "part_number": part_number,
                "supplier_code": supplier_code,
                "supplier_part_number": part_number,
                "supplier_cost": record["cost"],
                "is_preferred": True # default to preferred for MVP
            }

    # Return rows in a stable sorted order for cleaner diffs and debugging
    return [
        unique_part_suppliers[relationship_key]
        for relationship_key in sorted(unique_part_suppliers)
    ]

def export_part_suppliers_to_csv(part_suppliers, output_path):
    """
    Exports normalized part-supplier relationships to a CSV file.
    """
    output_columns = [
        "part_number",
        "supplier_code",
        "supplier_part_number",
        "supplier_cost",
        "is_preferred"
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=output_columns)
        writer.writeheader()

        for part_supplier in part_suppliers:
            writer.writerow(part_supplier)

if __name__ == "__main__":
    records = load_records_from_csv(INPUT_CSV_PATH)
    part_suppliers = extract_part_suppliers(records)

    export_part_suppliers_to_csv(part_suppliers, OUTPUT_CSV_PATH)
    
    print(f"Total inventory records loaded: {len(records)}")
    print(f"Unique part-supplier relationships found: {len(part_suppliers)}")
    print(f"Part-suppliers CSV exported: {OUTPUT_CSV_PATH}")

    print("\nFirst 5 part-supplier relationships:")
    for part_supplier in part_suppliers[:5]:
        print(part_supplier)
