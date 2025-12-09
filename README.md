## Overview

OOP-built backend using Python for a simple online store. This project provides a terminal-based interface to:
- Create a customer account
- browse a product catalogue
- add/remove items from a shopping cart 
- checkout and process payments (card / PayPal)
- persist orders and carts (MySQL-backed repository layer)

The codebase is organised with a clear separation between domain models, services, and repository/DB access. It is intended as a learning/demo backend rather than a production-ready service.

**This README** covers architecture, running locally, running with Docker, and the repository layout.

## Quick Start

### Docker (Recommended)

Run the interactive backend directly (attach a TTY):
```powershell
docker compose run --rm backend
```
MySQL database is seeded with two users:
- (**username**: as below, **password** = password)
- Customer: leo
- Staff: admin

### Local (Without Docker)

Create a .env file
```powershell
EXAMPLE:
HOST=localhost
USER=root
PASSWORD=password
DATABASE=online_store_database
POOL_SIZE=5
```

Create a Python virtualenv and install dependencies:
```powershell
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate
pip install -r Backend/requirements.txt
python Backend/main.py
```

Note: The backend expects a MySQL database running locally on port 3306. See `Backend/db/init` for init MySQL database schema and seed.

## Running & Interactivity

When interacting with Docker — run the `backend` service with a TTY (from the project root `docker compose run --rm backend`) so you can type responses for the CLI prompts.

**Do not use** `docker compose up -d` (detached mode) for an interactive CLI app — you won't be able to provide input.

## Environment Configuration

**Docker environment variables** (set in `docker-compose.yml`):
- `MYSQL_ROOT_PASSWORD` — root DB password (set for MySQL container)
- `MYSQL_DATABASE` — database name created by MySQL container (default: `online_store`)
- `MYSQL_USER`, `MYSQL_PASSWORD` — optional DB user created on initialization
- `HOST` — database host (Docker service name: `MySQL`)
- `USER` — database user (default: `appuser`)
- `PASSWORD` — database password
- `NAME` — database name (default: `online_store`)
- `POOL_SIZE` — connection pool size (default: 5)

## Database Setup

If DB init scripts change: the MySQL image runs SQL files in `Backend/db/init` only when the volume is empty. To re-run init scripts:

```powershell
docker compose down
docker volume rm online-store-backend_db_data
docker compose run --rm backend
```

To inspect the database inside a running container:
```powershell
# Find mysql_container_id
docker ps
# Exec into container
docker exec -it <mysql_container_id> sh
# Inside container:
mysql -p (password: Pa55w.rd)
USE online_store;
SHOW TABLES;
```

## Architecture & Design

### Layers

- **Presentation**: `Backend/main.py` (terminal CLI, user menu)
- **Models**: `Backend/models/` (domain objects: `Cart`, `Order`, `Item`, `User`, `Catalogue`)
- **Services**: `Backend/services/` (business logic: `CartService`, `OrderService`, `PaymentService`, `TransactionFacade`)
- **Repositories**: `Backend/db/repositories/` (SQL access wrappers, data persistence)
- **DB Connection**: `Backend/db/connection/` (connection pooling and cursor helpers)
- **Utilities**: `Backend/utlities/` (helper functions, formatting)

### Design Patterns

- **Singleton**: `Catalogue` — ensures a single instance of the product list
- **Factory**: `PaymentFactory` — creates payment implementations (Card, PayPal)
- **Strategy / Polymorphism**: Payment implementations in `Backend/models/PAYMENT/`
- **Facade**: `TransactionFacade` — orchestrates checkout, payment, and sales workflows
- **Repository**: `Backend/db/repositories/` — abstracts DB access from services

## Directory Structure

```
.
├── docker-compose.yml
├── README.md
├── Backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   ├── db/
│   │   ├── connection/
│   │   │   ├── config.py
│   │   │   ├── connection.py
│   │   │   └── helper.py
│   │   ├── init/
│   │   │   ├── 001-schema.sql
│   │   │   └── 002-seed.sql
│   │   └── repositories/
│   │       ├── cart_repository.py
│   │       ├── item_repository.py
│   │       ├── transaction_repository.py
│   │       └── user_repository.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cart.py
│   │   ├── catalogue.py
│   │   ├── item.py
│   │   ├── order.py
│   │   ├── sales_document.py
│   │   ├── user.py
│   │   └── PAYMENT/
│   │       ├── CardPayment.py
│   │       ├── CardPaymentMethod.py
│   │       ├── Payment.py
│   │       ├── PaymentMethod.py
│   │       ├── PaypalPayment.py
│   │       └── PaypalPaymentMethod.py
│   ├── services/
│   │   ├── cart_service.py
│   │   ├── catalogue_service.py
│   │   ├── order_service.py
│   │   ├── payment_factory.py
│   │   ├── payment_service.py
│   │   ├── sales_service.py
│   │   ├── transaction_facade.py
│   │   └── user_service.py
│   └── utlities/
│       └── format_items_table.py
```

## Troubleshooting

### Backend cannot connect to database
- Ensure the MySQL container is healthy: `docker compose ps`
- Check logs: `docker compose logs MySQL` or `docker compose logs backend`
- Verify DB is seeded: exec into the container and query the `user` table

### Cannot type input in Docker
- Use `docker compose run --rm backend` instead of `docker compose up backend`

### Need to remove docker containers & volume
```powershell
exit terminal application
docker compose down
docker volume rm online-store-backend_db_data
```