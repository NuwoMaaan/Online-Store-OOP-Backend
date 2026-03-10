from sqlalchemy import inspect
from db.connection.session import get_session
from db.connection.connection import engine
from db.models import Base, User, Item
from config import settings


def db_initialized():
    inspector = inspect(engine)
    return "users" in inspector.get_table_names()


def init_db():
    print("Ensuring tables exist...")
    Base.metadata.create_all(bind=engine)


def seed_data():
    with get_session() as db:

        # Admin seed
        if not db.query(User).filter_by(username=settings.ADMIN_USER).first():
            admin = User(
                username=settings.ADMIN_USER,
                password=settings.ADMIN_PASSWORD,
                role="admin",
                email="admin@outlook.com"
            )
            db.add(admin)
            print("Admin user added.")

        # Catalogue seed
        if db.query(Item).count() == 0:
            items = [
                Item(name="Iphone", price=999.99, quantity=50),
                Item(name="Keyboard", price=39.99, quantity=50),
                Item(name="Monitor", price=450.00, quantity=50),
                Item(name="Headphones", price=370.00, quantity=50),
                Item(name="Ipad", price=870.00, quantity=50),
                Item(name="Macbook", price=1870.00, quantity=50),
                Item(name="Airpods", price=220.00, quantity=50),
            ]
            db.add_all(items)
            print("Catalogue items seeded.")


def initialize_database():
    init_db()

    if not db_initialized():
        print("Database empty. Running seed.")
        seed_data()
    else:
        print("Database already initialized. Skipping seed.")


if __name__ == "__main__":
    initialize_database()