# services/order_service.py

import json
from models.order import Order, OrderItem
from services.cart_service import CartService
from services.product_service import ProductService

class OrderService:
    def __init__(self, db_path="db/order_data.json"):
        self.db_path = db_path
        self.orders = self.load_orders()
        self.cart_service = CartService()
        self.product_service = ProductService()

    def load_orders(self):
        try:
            with open(self.db_path, "r") as f:
                data = json.load(f)
                return [Order.from_dict(o) for o in data.get("orders", [])]
        except FileNotFoundError:
            return []

    def save_orders(self):
        with open(self.db_path, "w") as f:
            json.dump({"orders": [o.to_dict() for o in self.orders]}, f, indent=4)

    def place_order(self, user_id: int):
        cart = self.cart_service.get_cart_by_user_id(user_id)
        if not cart.items:
            raise ValueError("Cart is empty.")

        total_price = 0
        order_items = []

        for item in cart.items:
            product = self.product_service.get_product_by_id(item.product_id)
            if not product or product.stock < item.quantity:
                raise ValueError(f"Product ID {item.product_id} is out of stock or unavailable.")
            self.product_service.reduce_stock(product.id, item.quantity)
            total_price += product.price * item.quantity
            order_items.append(OrderItem(item.product_id, item.quantity))

        order_id = len(self.orders) + 1
        new_order = Order(order_id, user_id, order_items, total_price)
        self.orders.append(new_order)
        self.save_orders()
        self.cart_service.clear_user_cart(user_id)

        return new_order

    def get_order_by_id(self, order_id: int):
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None

    def get_orders_by_user(self, user_id: int):
        return [order for order in self.orders if order.user_id == user_id]
