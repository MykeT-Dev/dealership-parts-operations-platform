import csv

INPUT_CSV_PATH = "data/processed/parts_inventory_clean.csv"
OUTPUT_CSV_PATH = "data/processed/categories_clean.csv"

def load_records_from_csv(file_path):
    """
    Loads records from the cleaned CSV file into a list of dictionaries
    """

    records = []

    with open(file_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            records.append(row)

    return records

def extract_unique_categories(records):
    """
    Extracts unique category codes from inventory records.
    Returns a sorted list of category dictionaries.
    """
    unique_category_codes = set()

    for record in records:
        # Pull the category code from each row
        category_code = record["category_code"].strip()

        # Only include non-empty values
        if category_code:
            unique_category_codes.add(category_code)

    categories = []

    # Sort for consistent output
    for category_code in sorted(unique_category_codes):
        categories.append({
            "category_code": category_code,
            "name": category_code # placeholder for now
        })

    return categories

def export_categories_to_csv(categories, output_path):
    """
    Exports unique categories to a CSV file.
    """
    output_columns = ["category_code", "name"]

    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=output_columns)
        writer.writeheader()

        for category in categories:
            writer.writerow(category)

if __name__ == "__main__":
    records = load_records_from_csv(INPUT_CSV_PATH)
    categories = extract_unique_categories(records)

    export_categories_to_csv(categories, OUTPUT_CSV_PATH)

    print(f"Total inventory records loaded: {len(records)}")
    print(f"Unique categories found: {len(categories)}")
    print(f"Category CSV exported: {OUTPUT_CSV_PATH}")

    print("\nFirst 5 categories:")
    for category in categories[:5]:
        print(category)