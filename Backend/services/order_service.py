from __future__ import annotations
from utlities.format_items_table import print_items_table
from db.repositories.transaction_repository import insert_order, insert_order_items, reduce_stock
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.order import Order

class OrderService():
    @staticmethod
    def insert_order(order, db) -> bool:
        order_id = insert_order(order, db)
        if not order_id:
            return False
        
        order.order_no = order_id
        if insert_order_items(order_id, order.items, db):
            return True
        return False
    
    
    @staticmethod
    def reduce_stock(order, db) -> bool:
        return reduce_stock(order, db)

    @staticmethod
    def checkout(user) -> Order:
        if not user.cart.items:
            print("\nCart is empty. Please add items to your cart before checkout.")
            return None
        order = user.cart.checkout()
        order.order_summary()
        return order
    

    @staticmethod
    def order_summary(order) -> None:
        print("\n------Order Summary------:")
        print(f"Customer ID: {order.customer_id}")
        print("Shipping details:")
        for key,value in order.shipping_details.items():
            print(f"{key}: {value}")
        print("Items:")
        print_items_table(order.items)
        print(f"Total: ${order.total:.2f}")