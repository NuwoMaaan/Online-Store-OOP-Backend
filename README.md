## Overview

OOP-built backend using Python for a simple online store. This project provides a terminal-based interface to:
- Create a customer account
- browse a product catalogue
- add/remove items from a shopping cart
- add/remove items from catalogue (admin)
- checkout and process payments
- persist orders and carts 

The project has a focus on scalable and clean design & architecture when building systems. The project follows a service-oriented architecture with domain and database logic separated from class models and repositioned in service & repository layer. Technologies; MySQL relation-database, SQL Alchemy ORM, and Docker.

(Note: This is not a production-level system and is only for demo & learning purposes)

## Quick Start

### Docker (Recommended)

Run the interactive backend directly (attach a TTY):
```
docker compose run --rm backend
```
Backend may fail to connect to MySQL container because it is not yet healthly, rerun the same command to attempt restart. Alternatively, start the MySQL container separately first.

MySQL database is seeded with two users:
- (**username**: as below, **password** = password)
- Customer: leo
- Staff: admin

## Running & Interactivity

When interacting with Docker — run the `backend` service with a TTY (from the project root `docker compose run --rm backend`) so you can type responses for the CLI prompts.

**Do not use** `docker compose up -d` (detached mode) for an interactive CLI app — you won't be able to provide input.

## Database 

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
SELECT * FROM <table>;
```

## Architecture & Design

### Layers

- **Presentation**: `Backend/main.py` (terminal CLI, user menu)
- **Models**: `Backend/models/` (domain objects: `Cart`, `Order`, `Item`, `User`, `Catalogue`)
- **Services**: `Backend/services/` (business logic: `CartService`, `OrderService`, `PaymentService`, `TransactionFacade`)
- **Repositories**: `Backend/db/repositories/` (SQL access wrappers, data persistence)
- **DB Connection**: `Backend/db/connection/` (ORM session context)
- **Utilities**: `Backend/utlities/` (helper functions, formatting)

### Design Patterns

- **Singleton**: `Catalogue` — ensures a single instance of the product list
- **Factory**: `PaymentFactory` — creates payment implementations (Card, PayPal)
- **Strategy / Polymorphism**: Payment implementations in `Backend/models/PAYMENT/`
- **Facade**: `TransactionFacade` — orchestrates checkout, payment, and sales workflows
- **Repository**: `Backend/db/repositories/` — abstracts DB access from services
- **Dependency injection**: `SQL Alchemy Session` - pass in database session context into functions

## Directory Structure

```
.
├── docker-compose.yml
├── README.md
├── Backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── config.py
│   ├── init.py
│   ├── tests/
│   ├── db/
│   │   ├── models.py
│   │   ├── connection/
│   │   │   ├── connection.py
│   │   │   └── session.py
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
- Check logs: `docker compose logs mysql` or `docker compose logs backend`
- Verify DB is seeded: exec into the container and query the `user` and `item` table

### Cannot type input in Docker
- Use `docker compose run --rm backend` instead of `docker compose up backend`

### Need to remove docker containers & volume
exit the terminal application (through menu or `ctrl + c`)
```powershell
docker compose down
docker volume rm online-store-backend_db_data
```
