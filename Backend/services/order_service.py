from __future__ import annotations
from utlities.format_items_table import print_items_table
from db.repositories.transaction_repository import check_stock, insert_order, insert_order_items, reduce_stock, remove_excess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.order import Order
    from models.user import User

class OrderService():
    @staticmethod
    def insert_order(order: Order, db) -> bool:
        order_id = insert_order(order, db)
        if not order_id:
            return False
        
        order.order_no = order_id
        if insert_order_items(order_id, order.items, db):
            return True
        return False
    
    @staticmethod
    def check_stock(order: Order, db) -> list[dict]:
        return check_stock(order, db)
    
    @staticmethod
    def reduce_stock(order: Order, db) -> bool:
        return reduce_stock(order, db)

    @staticmethod
    def checkout(user: User) -> Order:
        if not user.cart.items:
            print("\nCart is empty. Please add items to your cart before checkout.")
            return None
        order = user.cart.checkout()
        order.order_summary()
        return order
    
    @staticmethod
    def adjust_order_for_shortages(order: Order, shortages: list[dict]) -> None:
        for shortage in shortages:
            order.total -= shortage["missing"] * shortage["price"]
            remove_excess(order, shortage["item_id"], shortage["missing"])
    
    @staticmethod
    def adjust_order(shortages: list[dict]) -> bool | None:
        for shortage in shortages:
            name = shortage["name"] or f"Item {shortage['item_id']}"
            print(
                f"Insufficient stock for {name}. "
                f"Requested {shortage['requested']}, available {shortage['available']}."
            )
        choice = input("Continue with available stock? (y/n): ").strip().lower()
        if choice != "y":
            print("Checkout cancelled.")
            return None
        #self.adjust_order_for_shortages(order, shortages)
        return True

    @staticmethod
    def order_summary(order: Order) -> None:
        print("\n------Order Summary------:")
        print(f"Customer ID: {order.customer_id}")
        print("Shipping details:")
        for key,value in order.shipping_details.items():
            print(f"{key}: {value}")
        print("Items:")
        print_items_table(order.items)
        print(f"Total: ${order.total:.2f}")