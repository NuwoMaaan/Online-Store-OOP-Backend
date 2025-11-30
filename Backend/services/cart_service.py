import json
import os
from models.catalogue import Catalogue
from db.repositories.cart_repository import get_cart_by_user_id, delete_cart_by_cart_id, save_cart_by_cart_id

DATABASE_PATH = "Backend/db/mock/cart_data.json"

class CartService():
    @staticmethod
    def clear_cart_payment(cart_instance):
        cart = get_cart_by_user_id(cart_instance.customer_id)
        if cart:
            cart_id = cart["cart_id"]
            delete_cart_by_cart_id(cart_id)

    @staticmethod
    def save_cart(cart_instance):
        cart = get_cart_by_user_id(cart_instance.customer_id)
        if cart:
            cart_id = cart["cart_id"]
            save_cart_by_cart_id(cart_id, cart_instance.items)

    @staticmethod
    def load_cart(cart_instance):
        pass

        # need to implement 
        
        # with open(DATABASE_PATH, "r") as f:
        #     data = json.load(f)
        #     carts = data.get("carts", [])
        #     user_cart = next((cart for cart in carts if cart["customer_id"] == cart_instance.customer_id), None)
        #     if user_cart:
        #         catalogue = Catalogue.get_instance()
        #         cart_instance.items = []
        #         for item in user_cart["items"]:
        #             item_obj = catalogue.get_item_by_id(int(item["item_id"]))
        #             if item_obj:
        #                 cart_instance.items.append(item_obj)
        #     else:
        #         cart_instance.items = []
    
    @staticmethod
    def clear(cart):
        cart.clear_cart_payment()