import json
import os
from models.catalogue import Catalogue

DATABASE_PATH = "Backend/db/cart_data.json"

class CartService():

    @staticmethod
    def clear_cart_payment(cart_instance):
        with open(DATABASE_PATH, 'r') as f:
            data = json.load(f)
        carts = data.get("carts", [])
        carts = [cart for cart in carts if cart["customer_id"] != cart_instance.customer_id]
        carts.clear()
        data["carts"] = carts
        with open(DATABASE_PATH, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def save_cart(cart_instance):
        if os.path.exists(DATABASE_PATH):
            with open(DATABASE_PATH, "r") as f:
                data = json.load(f)
        else:
            data = {"carts": []}
        carts = data.get("carts", [])
        carts = [cart for cart in carts if cart["customer_id"] != cart_instance.customer_id]
        carts.append({
            "customer_id": cart_instance.customer_id,
            "items": [{"item_id": str(item.item_id)} for item in cart_instance.items]
        })
        data["carts"] = carts
        with open(DATABASE_PATH, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_cart(cart_instance):
        with open(DATABASE_PATH, "r") as f:
            data = json.load(f)
            carts = data.get("carts", [])
            user_cart = next((cart for cart in carts if cart["customer_id"] == cart_instance.customer_id), None)
            if user_cart:
                catalogue = Catalogue.get_instance()
                cart_instance.items = []
                for item in user_cart["items"]:
                    item_obj = catalogue.get_item_by_id(int(item["item_id"]))
                    if item_obj:
                        cart_instance.items.append(item_obj)
            else:
                cart_instance.items = []
    
    @staticmethod
    def clear(cart):
        cart.clear_cart_payment()