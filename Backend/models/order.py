import json
from pathlib import Path
from typing import List, Tuple
from models.cart import Cart
from models.item import Item

class Order:
    DATA_PATH = Path("database/orders.json")

    def __init__(self, order_id: int, customer_id: int, items: List[Item], shipping_address: str, shipping_cost: float):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.shipping_address = shipping_address
        self.shipping_cost = shipping_cost

    def calculate_total(self) -> float:
        return sum(price for _, price in self.items) + self.shipping_cost

    @classmethod
    def get_by_id(cls, order_id: int) -> "Order":
        with open(cls.DATA_PATH, "r") as f:
            orders = json.load(f)
        for o in orders:
            if o["order_id"] == order_id:
                return cls(
                    o["order_id"],
                    o["customer_id"],
                    o["items"],
                    o["shipping_address"],
                    o["shipping_cost"]
                )
        raise ValueError("Order not found.")

    @classmethod
    def create_from_cart(cls, cart: Cart, shipping_address: str, shipping_cost: float) -> "Order":
        if cls.DATA_PATH.exists():
            with open(cls.DATA_PATH, "r") as f:
                orders = json.load(f)
        else:
            orders = []

        new_id = len(orders) + 1
        new_order = {
            "order_id": new_id,
            "customer_id": cart.customer_id,
            "items": cart.get_items(),
            "shipping_address": shipping_address,
            "shipping_cost": shipping_cost
        }
        orders.append(new_order)

        with open(cls.DATA_PATH, "w") as f:
            json.dump(orders, f, indent=2)

        return cls(new_id, cart.customer_id, cart.get_items(), shipping_address, shipping_cost)
