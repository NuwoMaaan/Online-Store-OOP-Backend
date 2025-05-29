from models.item import Item
from typing import List

class Order:
    def __init__(self, customer_id, items, shipping_details):
        self.customer_id = customer_id
        self.items: List[Item] = []# List of Item objects
        self.shipping_details = shipping_details
        self.subtotal = sum(item.price for item in items)
        self.shipping_cost = 10.0
        self.total = self.subtotal + self.shipping_cost
        self.status = "pending"  # or "paid", "refund", "cancelled"
        self.payment = None      # IPayment object

    def add_payment(self, payment):
        self.payment = payment
        self.status = "paid"