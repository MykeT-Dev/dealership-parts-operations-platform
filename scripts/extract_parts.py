import csv

INPUT_CSV_PATH = "data/processed/parts_inventory_clean.csv"
OUTPUT_CSV_PATH = "data/processed/parts_clean.csv"

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

def extract_unique_parts(records):
    """
    Extracts unique part numbers from the cleaned inventory records.
    Returns a sorted list of part dictionaries.
    """

    unique_parts = {}

    for record in records:
        # Use part number as the unique identifier for MVP
        part_number = record["part_number"].strip()

        # Skip blank part numbers
        if not part_number:
            continue

        # Only keep the first occurrence of each part number
        if part_number not in unique_parts:
            unique_parts[part_number] = {
                "part_number": part_number,
                "description": record["description"].strip(),
                "category_code": record["category_code"].strip(),
                "quantity": record["quantity"],
                "public_price": record["price"],
            }

    # Return parts sorted by part number for stable output
    return [unique_parts[part_number] for part_number in sorted(unique_parts)]
    
def export_parts_to_csv(parts, output_path):
    """
    Exports deduplicated parts to a CSV file.
    """
    output_columns = [
        "part_number",
        "description",
        "category_code",
        "quantity",
        "public_price"
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=output_columns)
        writer.writeheader()

        for part in parts:
            writer.writerow(part)

if __name__ == "__main__":
    records = load_records_from_csv(INPUT_CSV_PATH)
    parts = extract_unique_parts(records)

    export_parts_to_csv(parts, OUTPUT_CSV_PATH)

    print(f"Total inventory records loaded: {len(records)}")
    print(f"Unique parts found: {len(parts)}")
    print(f"Parts CSV exported: {OUTPUT_CSV_PATH}")

    print("\nFirst 5 parts:")
    for part in parts[:5]:
        print(part)