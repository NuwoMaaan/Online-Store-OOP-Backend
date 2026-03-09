from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Integer, String, Numeric, ForeignKey, DateTime

from datetime import datetime


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)

class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int] = mapped_column(Integer)

class Cart(Base):
    __tablename__ = "cart"

    cart_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.user_id"),
        nullable=False
    )

class CartItems(Base):
    __tablename__ = "cart_items"

    cart_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("cart.cart_id"), 
        primary_key=True,
        nullable=False 
    )

    item_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("item.id"),
        primary_key=True,
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

class Orders(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.user_id"),
        nullable=False,
    )
    total: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    address: Mapped[str] = mapped_column(String(150), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[int] = mapped_column(String(4), nullable=False)

class OrderItems(Base):
    __tablename__ = "order_items"

    order_item_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )

    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False
    )

    item_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("item.id"),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_each: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    line_total: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    