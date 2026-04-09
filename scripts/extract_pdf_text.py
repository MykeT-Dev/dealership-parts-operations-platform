import pdfplumber

# Path to the PDF file
PDF_PATH = "data/parts_inventory.pdf"

def extract_lines_from_pdf(pdf_path):
    """
    Extracts all non-empty lines from the PDF to a flat list.
    """
    all_lines = []

    # Open the PDF file using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            # Extract text from the page
            text = page.extract_text()
            
            #skip pages that return no text
            if not text:
                continue

            # Split page into lines
            lines = text.split("\n")

            for line in lines:
                # Remove leading and trailing whitespace
                line = line.strip()

                # ignore empty lines
                if line: # Only add non-empty lines
                    all_lines.append(line)

    return all_lines

def classify_line(line):
    """
    Classifies each line so we know how to handle it later.

    Why:
    - Not every line is a part record
    - We must identify supplier headers, subtotals, and report noise
    """

    # Detect supplier headers
    if line.startswith("Supplier Code:") and "sub totals" not in line:
        return "supplier"
    
    # Detect subtotal lines
    if line.startswith("Supplier Code:") and "sub totals" in line:
        return "subtotal"
    
    # Detect report metadata / noise
    if (
        line.startswith("501 Parts Inventory")
        or line.startswith("Printed On:")
        or line.startswith("Group By:")
        or line.startswith("Filter:")
        or line.startswith("Part Number Description")
        or line.startswith("Page ")
        or line.startswith("Parts Inventory:")
    ):
        return "header"
    
    # Everything else is assumed to be a part line, will validate later
    return "part"

def clean_money_value(value):
    # Remove currency symbols and commas, then convert to float
    return float(value.replace("$", "").replace(",", ""))

def clean_percent_value(value):
    # Remove percent symbol and convert to float
    return float(value.replace("%", ""))


def parse_part_line(line):
    """
    Parses a single inventory line into structured fields.

    Expected pattern:
    [part_number] [description...] [supplier_code] [category_code]
    [qty] [cost] [price] [margin] [margin_percent]
    """
    tokens = line.split()

    # part_number + supplier + category + qty + cost + price + margin + margin%
    if len(tokens) < 8:
        return None
    
    # Parse fixed-position fields from the right side
    margin_percent_raw = tokens[-1]
    margin_raw = tokens[-2]
    price_raw = tokens[-3]
    cost_raw = tokens[-4]
    quantity_raw = tokens[-5]
    category_code = tokens[-6]
    supplier_code = tokens[-7]

    # Everything before the last 7 tokens contains: part number and description
    left_side = tokens[:-7]

    # Guard against malformed rows
    if len(left_side) < 2:
        return None
    
    # First token is the part number
    part_number = left_side[0]

    # Everything else is the description
    description = " ".join(left_side[1:])

    # Convert raw string values into normalized numeric types.
    # Quantity is parsed as float because the source data may contain
    # fractional values like 0.5.
    quantity = float(quantity_raw)
    cost = clean_money_value(cost_raw)
    price = clean_money_value(price_raw)
    margin = clean_money_value(margin_raw)
    margin_percent = clean_percent_value(margin_percent_raw)

    return {
        "part_number": part_number,
        "description": description,
        "supplier_code": supplier_code,
        "category_code": category_code,
        "quantity": quantity,
        "cost": cost,
        "price": price,
        "margin": margin,
        "margin_percent": margin_percent
    }


if __name__ == "__main__":
    # Extract lines from the PDF
    lines = extract_lines_from_pdf(PDF_PATH)

    # Tracks supplier from "Supplier Code:"
    current_supplier = None

    # Stores all parsed part data
    parsed_records = []

for line in lines:
    line_type = classify_line(line)

    # update supplier context when a new supplier section starts
    if line_type == "supplier":
        current_supplier = line.split(":")[1].strip()
        continue

    # Ignore headers, subtotals, and other non-part lines
    if line_type != "part":
        continue

    # Parse the current part line
    parsed = parse_part_line(line)

    if not parsed:
        continue
    # Store the supplier from the surrounding group for validation
    parsed["supplier_from_group"] = current_supplier

    parsed_records.append(parsed)

# Print the first 10 parsed records for verification
for record in parsed_records[:10]:
    print(record)