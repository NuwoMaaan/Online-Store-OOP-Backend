# models/cart.py
from typing import List
from models.item import Item
from models.cart_item import CartItem

class Cart:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.items: List[Item] = []

    @classmethod
    def from_dict(cls, data):
        cart = cls(data["user_id"])
        cart.items = [CartItem.from_dict(item) for item in data.get("items", [])]
        return cart

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "items": [item.to_dict() for item in self.items]
        }

    def add_item(self, item_id: str, price: float, quantity: int = 1):
        # If item exists, increase quantity
        for item in self.items:
            if item.item_id == item_id:
                item.quantity += quantity
                return
        # Otherwise add new item
        self.items.append(Item(item_id, price, quantity))

    def remove_item(self, item_id: str):
        self.items = [item for item in self.items if item.item_id != item_id]

    def clear_cart(self):
        self.items = []

    def get_items(self):
        return self.items

    def get_total(self):
        return sum(item.price * item.quantity for item in self.items)
