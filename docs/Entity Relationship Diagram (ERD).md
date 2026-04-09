# Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS {
        uuid id PK
        string email
        string hashed_password
        string role
    }

    PARTS {
        uuid id PK
        string part_number
        string description
        decimal public_price
        int quantity_on_hand
        uuid category_id FK
    }

    SUPPLIERS {
        uuid id PK
        string supplier_code
        string display_name
    }

    PART_SUPPLIERS {
        uuid id PK
        uuid part_id FK
        uuid supplier_id FK
        string supplier_part_number
        decimal supplier_cost
        int lead_time_days
        string availability_status
        boolean is_preferred
    }

    CATEGORIES {
        uuid id PK
        string name
        string slug
    }

    INVENTORY_ADJUSTMENTS {
        uuid id PK
        uuid part_id FK
        uuid user_id FK
        string adjustment_type
        int quantity_delta
        int previous_quantity
        int new_quantity
        string notes
    }

    CATEGORIES ||--o{ PARTS : categorizes
    PARTS ||--o{ PART_SUPPLIERS : has
    SUPPLIERS ||--o{ PART_SUPPLIERS : supplies
    PARTS ||--o{ INVENTORY_ADJUSTMENTS : tracks
    USERS ||--o{ INVENTORY_ADJUSTMENTS : creates