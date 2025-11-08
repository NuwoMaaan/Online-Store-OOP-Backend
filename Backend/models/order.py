from models.item import Item
from typing import List
import random
from services.order_service import OrderService


class Order:
    def __init__(self, customer_id, items, shipping_details):
        self.customer_id = customer_id
        self.items: List[Item] = items #List of Item objects
        self.shipping_details = shipping_details
        self.subtotal = sum(item.price for item in items)
        self.shipping_cost = 10.0
        self.total = self.subtotal + self.shipping_cost
        self.status = "pending"  # or "paid"
        self.payment = None      # IPayment object
        self.order_no = random.randint(2000,7000)

    def add_payment(self, payment):
        self.payment = payment
        self.status = "paid"

    def print_order_summary(self):
        OrderService.order_summary(self)

    def save_order_to_db(self, datetime):
        return OrderService.save_order_to_db(self, datetime)


    def to_dict(self, datetime):
        return {
            "order_no": self.order_no,
            "items": [{"item_id": item.item_id} for item in self.items],
            "shipping_details": self.shipping_details,
            "total": round(float(self.total), 2),
            "date": datetime.strftime("%Y-%m-%d %H:%M:%S") if hasattr(datetime, "strftime") else str(datetime)
        }
    
