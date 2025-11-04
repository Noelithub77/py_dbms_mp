# Restaurant Management System

A complete CRUD application built with Streamlit and MySQL that demonstrates all entity relationships from an ER diagram including 1:1, 1:N, and N:N relationships.

## Features

- **Complete CRUD Operations** for all entities
- **Relationship Management** across all entity types
- **Interactive UI** built with Streamlit
- **MySQL Backend** with proper foreign key constraints
- **Data Integrity** through relationship enforcement

## Entities

1. **Admin** - Manages restaurants and prepares food items
2. **Restaurant** - Managed by admins, receives orders
3. **Food** - Prepared by admins, part of orders
4. **Customer** - Places orders and initiates payments
5. **Order** - Links customers, restaurants, foods, and payments
6. **Payment** - Initiated by customers for orders

## Relationships

- Admin manages Restaurant (1:1)
- Admin prepares Food (1:N)
- Customer places Order (1:N)
- Customer initiates Payment (1:N)
- Food in Order (N:N via OrderFood junction table)
- Order linked to Payment (N:1)

## Setup

### 1. Install Dependencies

```bash
uv sync
```

### 2. Setup MySQL Database

Ensure MySQL server is running, then execute the schema:

```bash
mysql -u root -p < src/sql/schema.sql
```

Or import manually:
1. Open MySQL client
2. Run the contents of `src/sql/schema.sql`

### 3. Run Application

```bash
uv run streamlit run src/app.py
```

## Usage

### Database Connection

1. Launch the application
2. In the sidebar, enter your MySQL credentials:
   - Host (default: localhost)
   - User (default: root)
   - Password
   - Database (default: restaurant_db)
3. Click "Connect to Database"

### CRUD Operations

Navigate through entities using the sidebar menu. Each entity has four tabs:

- **Create** - Add new records
- **View** - Display all records with relationships
- **Update** - Modify existing records
- **Delete** - Remove records

### Example Workflow

1. **Create Admin** first (required for restaurants and food)
2. **Create Restaurant** and assign to admin
3. **Create Food items** and assign to admin
4. **Create Customers**
5. **Create Payment** for a customer
6. **Create Order** linking customer, restaurant, and payment
7. **Add Foods to Order** to demonstrate N:N relationship

## Project Structure

```
src/
├── app.py                    # Main Streamlit application
├── sql/
│   ├── schema.sql           # DDL for all tables
│   └── db_operations.py     # Database operations classes
└── ui/
    └── crud_components.py   # UI components for each entity
```

## Database Schema

The schema includes:
- 6 main entity tables
- 1 junction table (OrderFood) for N:N relationship
- Foreign key constraints for referential integrity
- Indexes for performance optimization
- Cascading deletes where appropriate

## Technologies

- **Frontend**: Streamlit
- **Backend**: MySQL
- **Python**: 3.12+
- **Package Manager**: uv
- **Database Driver**: mysql-connector-python
