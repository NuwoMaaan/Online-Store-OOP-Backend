# models/cart.py
from typing import List
from models.cart_item import CartItem  # You should use CartItem, not Item here

class Cart:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.items: List[CartItem] = []

    @classmethod
    def from_dict(cls, data: dict) -> "Cart":
        cart = cls(data["user_id"])
        cart.items = [CartItem.from_dict(item) for item in data.get("items", [])]
        return cart

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "items": [item.to_dict() for item in self.items]
        }

    def add_item(self, item_id: int, price: float, quantity: int = 1):
        for item in self.items:
            if item.item_id == item_id:
                item.quantity += quantity
                return
        self.items.append(CartItem(item_id=item_id, price=price, quantity=quantity))

    def remove_item(self, item_id: int):
        self.items = [item for item in self.items if item.item_id != item_id]

    def clear_cart(self):
        self.items = []

    def get_items(self) -> List[CartItem]:
        return self.items

    def get_total(self) -> float:
        return sum(item.price * item.quantity for item in self.items)
