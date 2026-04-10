import csv
from pathlib import Path

INPUT_CSV_PATH = "data/processed/parts_inventory_clean.csv"
OUTPUT_CSV_PATH = "data/processed/suppliers_clean.csv"

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

def extract_unique_suppliers(records):
    """
    Extracts unique supplier codes from the cleaned inventory records.
    Returns a sorted list of supplier dictionaries.
    """

    unique_supplier_codes = set()

    for record in records:
        supplier_code = record["supplier_code"].strip()

        if supplier_code:
            unique_supplier_codes.add(supplier_code)

    suppliers = []

    for supplier_code in sorted(unique_supplier_codes):
        suppliers.append({
            "supplier_code": supplier_code,
            "display_name": supplier_code
        })

    return suppliers

def export_suppliers_to_csv(suppliers, output_path):
    """
    Exports unique suppliers to a CSV file.
    """

    output_columns = ["supplier_code", "display_name"]

    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=output_columns)
        writer.writeheader()

        for supplier in suppliers:
            writer.writerow(supplier)

if __name__ == "__main__":
    records = load_records_from_csv(INPUT_CSV_PATH)
    suppliers = extract_unique_suppliers(records)

    export_suppliers_to_csv(suppliers, OUTPUT_CSV_PATH)

    print(f"Total inventory records loaded: {len(records)}")
    print(f"Unique suppliers found: {len(suppliers)}")
    print(f"Supplier CSV exported: {OUTPUT_CSV_PATH}")

    print("\nFirst 5 suppliers:")
    for supplier in suppliers[:5]:
        print(supplier)