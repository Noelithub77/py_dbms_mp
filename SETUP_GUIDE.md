# Quick Setup Guide

## Prerequisites

1. MySQL Server installed and running
2. Python 3.12+
3. uv package manager

## Step-by-Step Setup

### 1. Install Dependencies (Already Done)

```bash
uv sync
```

### 2. Create Database

Open MySQL client:

```bash
mysql -u root -p
```

Then run:

```sql
SOURCE src/sql/schema.sql;
```

Or alternatively:

```bash
mysql -u root -p < src/sql/schema.sql
```

This will:
- Drop existing `restaurant_db` (if exists)
- Create new `restaurant_db` database
- Create all tables with relationships
- Set up foreign keys and indexes

### 3. Run the Application

```bash
uv run streamlit run src/app.py
```

Or simply:

```bash
uv run python src/main.py
```

### 4. Configure Database Connection

In the Streamlit app:

1. Enter MySQL credentials in sidebar:
   - Host: `localhost`
   - User: `root`
   - Password: `[your password]`
   - Database: `restaurant_db`

2. Click "Connect to Database"

### 5. Start Using CRUD Operations

Follow this order for best results:

1. **Admin** - Create at least one admin
2. **Restaurant** - Create restaurants and link to admin
3. **Food** - Add food items and link to admin
4. **Customer** - Create customer accounts
5. **Payment** - Create payments for customers
6. **Order** - Create orders linking all entities
   - Add foods to orders (N:N relationship)

## Troubleshooting

### Connection Error

If you get connection errors:
- Ensure MySQL server is running
- Check credentials are correct
- Verify database exists: `SHOW DATABASES;`

### Import Error

If modules not found:
- Run `uv sync` again
- Ensure you're in project directory
- Use `uv run` prefix for commands

### Foreign Key Constraint Error

If you get FK errors when deleting:
- Delete dependent records first
- Or check cascade rules in schema.sql

## Testing Relationships

### 1:1 (Admin manages Restaurant)
- Create admin → Create restaurant → Assign admin
- Each restaurant can have only one admin

### 1:N (Admin prepares Food)
- One admin can prepare many foods
- Create multiple foods with same admin

### 1:N (Customer places Orders)
- One customer can place many orders
- Create multiple orders for same customer

### N:N (Food in Orders)
- Multiple foods can be in one order
- One food can be in multiple orders
- Use "Manage Order Foods" in Order Update tab

### N:1 (Orders to Payment)
- Multiple orders can share one payment
- Create payment → Link multiple orders to it

## Database Schema Info

Tables:
- `Admin` (id, username, password, email, address, phoneno)
- `Restaurant` (id, name, address, openingHours, admin_id)
- `Food` (id, name, ingredients, category, isNonVeg, admin_id)
- `Customer` (id, username, password, email, address, phoneno)
- `Payment` (id, type, price, customer_id)
- `Order` (id, price, address, customer_id, restaurant_id, payment_id)
- `OrderFood` (order_id, food_id, quantity) - Junction table

All tables have timestamps and appropriate indexes.
