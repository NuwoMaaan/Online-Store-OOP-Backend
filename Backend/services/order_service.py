import os
import json
from utlities.format_items_table import print_items_table

db_file="Backend/db/order_data.json"

class OrderService():

    @staticmethod
    def save_order_to_db(order, datetime):
        if os.path.exists(db_file):
            with open(db_file, "r") as f:
                data = json.load(f)
        else:
            data = {"ordersDB": []}
        # Find user entry or create new
        user_entry = next((u for u in data["ordersDB"] if u["customer_id"] == order.customer_id), None)
        order_dict = order.to_dict(datetime)
        if user_entry:
            user_entry["orders"].append(order_dict)
        else:
            data["ordersDB"].append({
                "customer_id": order.customer_id,
                "orders": [order_dict]
            })
        with open(db_file, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def checkout(user):
        order = user.cart.checkout()
        order.order_summary()
        return order
    
    @staticmethod
    def order_summary(order):
        print("\n------Order Summary------:")
        print(f"Order Number: #{order.order_no}")
        print(f"Customer ID: {order.customer_id}")
        print("Shipping details:")
        for key,value in order.shipping_details.items():
            print(f"{key}: {value}")
        print("Items:")
        print_items_table(order.items)
        print(f"Total: ${order.total:.2f}")


    
# EXAMPLE STRUCTURE OF ORDERS IN DB
# {
#   "ordersDB": [
#         {
#       "customer_id": 1,
#       "orders": [
#         {
#           "order_no": 101,
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