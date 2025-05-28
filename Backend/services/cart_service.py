import json
from models.cart import Cart

class CartService:
    def __init__(self, db_path="db/cart_data.json"):
        self.db_path = db_path
        self.carts = self.load_carts()

    def load_carts(self):
        try:
            with open(self.db_path, "r") as f:
                data = json.load(f)
                return [Cart.from_dict(c) for c in data.get("carts", [])]
        except FileNotFoundError:
            return []

    def save_carts(self):
        with open(self.db_path, "w") as f:
            json.dump({"carts": [c.to_dict() for c in self.carts]}, f, indent=4)

    def get_cart_by_user_id(self, user_id: int):
        for cart in self.carts:
            if cart.user_id == user_id:
                return cart
        new_cart = Cart(user_id)
        self.carts.append(new_cart)
        return new_cart

    def add_to_cart(self, user_id: int, item_id: str, price: float, quantity: int = 1):
        cart = self.get_cart_by_user_id(user_id)
        cart.add_item(item_id, price, quantity)
        self.save_carts()
        return cart

    def remove_from_cart(self, user_id: int, item_id: str):
        cart = self.get_cart_by_user_id(user_id)
        cart.remove_item(item_id)
        self.save_carts()
        return cart

    def clear_user_cart(self, user_id: int):
        cart = self.get_cart_by_user_id(user_id)
        cart.clear_cart()
        self.save_carts()
        return cart
