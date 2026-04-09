# Data Cleaning / Sanitization Document

## 1. Overview

This project uses a **real-world dealership parts inventory export** as its source dataset.

The source data is provided as a **PDF report**, not a structured data file. Because of this, the dataset must be **extracted, cleaned, normalized, and sanitized** before it can be used in a production-style application.

The goal is to transform raw operational data into a:

- clean
- normalized
- portfolio-safe
- production-ready dataset

The cleaned dataset is specifically structured to align with the system's relational schema (ERD).

---

## 2. Source Data Description

The source file is a PDF export titled:

> "501 Parts Inventory"

The report is:

- grouped by **supplier code**
- filtered where **Active State = True**
- formatted for **human readability, not machine processing**

### Fields observed in the source

- Part Number
- Description
- Source (Supplier Code)
- Category Code
- Quantity
- Cost
- Price
- Margin
- Margin %

---

## 3. Problems Identified in Source Data

### 3.1 PDF Format (Non-Structured Data)

- Data is embedded in text layout
- Rows are not reliably delimited
- Some records span multiple lines

### 3.2 Supplier Representation

- Suppliers are represented as short codes (e.g., `YA`, `CHF`, `LS`)
- No dedicated supplier table exists
- Supplier grouping is implicit, not relational

### 3.3 Category Inconsistency

- Categories appear as abbreviated internal codes (e.g., `ACC`, `PM5`, `AMS`)
- Not human-readable
- Not normalized
- Often unreliable or defaulted

### 3.4 Duplicate / Variant Part Numbers

- Some entries contain multiple part numbers in one row
- Some part numbers appear with suffix variations (e.g., `-EXTRA`, `W`)
- Indicates lack of normalized product identity

### 3.5 Financial Data Issues

#### Stored Margin Fields

- Margin and Margin % are precomputed in the dataset
- These values may be inconsistent or stale
- These values will **not** be used as a source of truth

#### Zero-Value Records

- Many rows contain:
  - `0.00` cost
  - `0.00` price
  - `0.00` margin
- These may represent:
  - inactive pricing
  - placeholder records
  - incomplete data

### 3.6 Formatting Issues

- Commas in numeric values (e.g., `1,879.00`)
- Quoted descriptions
- Inconsistent casing and spacing
- Special characters in descriptions

---

## 4. Data Extraction Strategy

The PDF will be processed using a **custom Python parser**.

### Extraction Goals

- Convert PDF text into structured rows
- Output intermediate format (CSV or JSON)
- Preserve raw values for traceability

### Extracted Raw Fields

- raw_part_number
- raw_description
- raw_supplier_code
- raw_category_code
- raw_quantity
- raw_cost
- raw_price
- raw_margin
- raw_margin_percent

---

## 5. Data Transformation Strategy

The transformation process converts raw extracted data into a structure aligned with the ERD.

### 5.1 Parts Table Mapping

Mapped fields:

- part_number → raw_part_number
- description → raw_description
- public_price → raw_price
- quantity_on_hand → raw_quantity
- category_id → derived from normalized categories (optional)

Notes:

- `part_number` is treated as the unique identity for MVP
- Cost is **not** stored on the `parts` table
- Margin values are **not** stored
- Parts represent the canonical product identity

### 5.2 Suppliers Table Mapping

Mapped fields:

- supplier_code → raw_supplier_code
- display_name → anonymized value

Notes:

- Supplier codes are normalized into a dedicated table
- Supplier identities are anonymized for safe public use

### 5.3 Part Suppliers Table Mapping

Mapped fields:

- part_id → linked from parts
- supplier_id → linked from suppliers
- supplier_cost → raw_cost
- supplier_part_number → extracted where possible
- lead_time_days → optional (future/manual)
- availability_status → optional (future/manual)
- is_preferred → default or manually assigned

Notes:

- This table is the source of truth for cost
- Enables multiple suppliers per part
- Internal margin calculations are based on `supplier_cost`
- This design intentionally separates cost from parts for normalization

### 5.4 Categories Table Mapping

Mapped fields:

- name → derived from raw_category_code
- slug → generated from name

Notes:

- Categories are optional and loosely enforced
- Codes are normalized to readable values where possible
- Some categories may be grouped or simplified

### 5.5 Inventory Adjustments

Not derived from source data.

Notes:

- Populated through application logic
- Tracks all inventory changes over time
- Adjustment types include:
  - sold
  - manual_correction
  - received
  - returned

---

## 6. Financial Data Handling

### Cost

- Stored per supplier in `part_suppliers.supplier_cost`
- Original values may be adjusted or sanitized
- Not exposed publicly

### Price

- Stored as `public_price` on parts
- Represents customer-facing pricing

### Margin

- **Not stored** in the database
- Calculated dynamically in backend logic

Example formulas:

```python
margin = public_price - supplier_cost
margin_percent = (margin / public_price) * 100
```

---

## 7. Data Sanitization Rules

To ensure safe public use:

- Supplier identities are anonymized
- Cost values are modified to remove sensitive data
- Margin is calculated from sanitized values
- Dataset remains realistic but not confidential

---

## 8. Output Dataset Goals

The cleaned dataset will:

- map directly to ERD tables
- support normalized relational structure
- enforce public vs internal data separation
- be safe for portfolio use
- reflect real-world business logic

---

## 9. Relationship to System Design

The cleaned dataset feeds directly into:

- database schema (ERD)
- backend models
- API responses
- frontend rendering

The raw PDF is treated strictly as:

> source material — not the system design

---