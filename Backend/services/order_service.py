import os
import json

db_file="Backend/db/order_data.json"

class OrderService():
    
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

    
