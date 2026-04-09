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
    margin_percent = tokens[-1]
    margin = tokens[-2]
    price = tokens[-3]
    cost = tokens[-4]
    quantity = tokens[-5]
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

    # # Only keep lines that look like part records
    part_lines = [line for line in lines if classify_line(line) == "part"]

    # Parse and print the first 10 records for verification
    for line in part_lines[:10]:
        parsed = parse_part_line(line)
        print(parsed)