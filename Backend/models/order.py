from models.item import Item
from typing import List
import random
from models.format_items_table import print_items_table
import json
import os


db_file="Backend/db/order_data.json"

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

    def order_summary(self):
        print("\n------Order Summary------:")
        print(f"Order Number: #{self.order_no}")
        print(f"Customer ID: {self.customer_id}")
        print("Shipping details:")
        for key,value in self.shipping_details.items():
            print(f"{key}: {value}")
        print("Items:")
        print_items_table(self.items)
        print(f"Total: ${self.total:.2f}")
         

    def save_order_to_db(self, datetime):
        if os.path.exists(db_file):
            with open(db_file, "r") as f:
                data = json.load(f)
        else:
            data = {"ordersDB": []}
        # Find user entry or create new
        user_entry = next((u for u in data["ordersDB"] if u["customer_id"] == self.customer_id), None)
        if user_entry:
            user_entry["orders"].append(self.to_dict(datetime))
        else:
            data["ordersDB"].append({
                "customer_id": self.customer_id,
                "orders": [self.to_dict(datetime)]
            })
        with open(db_file, "w") as f:
            json.dump(data, f, indent=4)

    def to_dict(self, datetime):
            return {
                "order_no": self.order_no,
                "items": [{"item_id": item.item_id} for item in self.items],
                "shipping_details": self.shipping_details,
                "total": round(float(self.total), 2),
                "date": datetime.strftime("%Y-%m-%d %H:%M:%S") if hasattr(datetime, "strftime") else str(datetime)
            }



# {
#   "ordersDB": [
#         {
#       "customer_id": 1,
#       "orders": [
#         {
#           "order_id": 101,
#           "items": [
#             {"item_id": 2},
#             {"item_id": 5}
#           ],
#           "shipping_details": {
#             "address": "123 Main St",
#             "city": "Melbourne",
#             "postal_code": "3000"
#           },
#           "total": 1549.98,
#           "date": "2025-06-03 04:20:18"
#         }
#       ]
#     }
#   ]
# }