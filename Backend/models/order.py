from models.item import Item
from typing import List
import random

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
        self.order_no = random.randint(2000,4000)

    def add_payment(self, payment):
        self.payment = payment
        self.status = "paid"

    def order_summary(self):
        print("\n-----Order Summary-----:")
        print(f"Order Number: #{self.order_no}")
        print(f"Customer ID: {self.customer_id}")
        print("Shipping details:")
        for key,value in self.shipping_details.items():
            print(f"{key}: {value}")
        for item in self.items:
            print(f"- {item.name}: ${item.price:.2f}")
        print(f"Total: ${self.total:.2f}")  

