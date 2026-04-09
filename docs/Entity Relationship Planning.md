
# Entity Relationship Planning

## Overview

This document defines the core database structure for the Dealership Parts Operations Platform.

The schema is designed based on:

- real-world dealership workflow
- normalized relational design
- separation of public vs internal data
- supplier-dependent cost structure
- inventory tracking via adjustments

This ERD reflects **MVP scope only** and intentionally avoids overengineering.

---

## Access Control Model

The system defines three levels of access:

### Public (Unauthenticated)

No login required.

Can:

- browse parts
- search and filter parts
- view public pricing
- view simplified stock availability

Cannot:

- access internal data
- modify any records
- view cost or margin
- create inventory adjustments

### User (Authenticated)

Represents internal staff performing day-to-day operations.

Can:

- view all public information
- sell parts (reduces inventory)
- return parts (increases inventory)
- create inventory adjustment records for operational actions

Cannot:

- modify pricing
- manually override inventory counts
- view supplier cost
- view margin or margin percent

### Admin (Authenticated)

Represents elevated internal users with full system control.

Can:

- perform all User actions
- modify pricing
- manually adjust inventory
- manage parts, suppliers, and categories
- view supplier cost
- view margin and margin percent

---

## Core Entities

### 1. Users

#### Purpose

Stores authenticated internal users.

#### Fields

- id
- email
- hashed_password
- role (`user`, `admin`)
- is_active
- created_at
- updated_at

#### Notes

- Public users are not stored in the database
- Role determines authorization level
- Linked to inventory adjustments for audit tracking

---

### 2. Parts

#### Purpose

Represents the core inventory item.

#### Fields

- id
- part_number (unique)
- description
- public_price
- quantity_on_hand
- category_id (nullable)
- is_active
- created_at
- updated_at

#### Notes

- Part number is the canonical identity for MVP
- Cost is **not** stored here because it depends on supplier
- Quantity represents physical inventory available for use or sale

---

### 3. Suppliers

#### Purpose

Represents vendors/distributors used for sourcing parts.

#### Fields

- id
- supplier_code
- display_name (anonymized)
- is_active
- created_at
- updated_at

#### Notes

- Supplier represents where parts are ordered from
- Manufacturer is intentionally excluded in MVP

---

### 4. Part Suppliers

#### Purpose

Stores supplier-specific data for each part.

#### Fields

- id
- part_id (FK → parts)
- supplier_id (FK → suppliers)
- supplier_part_number (nullable)
- supplier_cost
- lead_time_days (nullable)
- availability_status (nullable)
- is_preferred
- is_active
- created_at
- updated_at

#### Notes

- Enables multiple suppliers per part
- Supplier-specific cost drives internal margin calculations
- Preferred supplier is used as the default source for cost calculations

---

### 5. Categories

#### Purpose

Optional grouping for browsing and filtering.

#### Fields

- id
- name
- slug
- is_active
- created_at
- updated_at

#### Notes

- Categories are optional and loosely enforced
- Primarily used for frontend filtering

---

### 6. Inventory Adjustments

#### Purpose

Tracks inventory changes over time.

#### Fields

- id
- part_id (FK → parts)
- user_id (FK → users, nullable)
- adjustment_type
- quantity_delta
- previous_quantity
- new_quantity
- notes (nullable)
- created_at

#### Adjustment Types (MVP)

- sold
- manual_correction
- received
- returned

#### Notes

- Provides audit history of inventory changes
- Quantity is updated on the part record and logged here

---

## Relationships

### One-to-Many

- One user → many inventory adjustments
- One part → many inventory adjustments
- One category → many parts

### Many-to-Many

- Parts ↔ Suppliers (via `part_suppliers`)

---

## Key Design Decisions

### Supplier-Dependent Cost

- Cost is stored per supplier
- Cost is not stored on `parts`

### Margin Calculation

- Margin is not stored
- Margin is calculated dynamically in backend logic

Example formulas:

- `margin = public_price - supplier_cost`
- `margin_percent = (margin / public_price) * 100`

### Inventory Model

- `quantity_on_hand` represents physical stock
- No reservation system in MVP
- All inventory changes are tracked via adjustments

### Categories

- Optional
- Used for filtering, not core business logic

---

## Out of Scope (MVP)

- manufacturer entity
- part supersession
- repair orders
- special orders
- reserved inventory
- purchase orders
- advanced pricing models
- multi-location inventory

---

## Status

ERD Draft v1 — Approved for implementation