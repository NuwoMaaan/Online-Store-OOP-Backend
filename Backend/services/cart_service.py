import json
import os
from models.catalogue import Catalogue
from db.repositories.cart_repository import get_cart_by_user_id, decrement_item_quantity, increment_item_quantity, remove_all_by_cart_id

DATABASE_PATH = "Backend/db/mock/cart_data.json"

class CartService():
    @staticmethod
    def clear_cart_payment(cart_instance):
        cart = get_cart_by_user_id(cart_instance.customer_id)
        if cart:
            cart_id = cart["cart_id"]
            remove_all_by_cart_id(cart_id)
    
    @staticmethod
    def remove_item(cart_instance, item_id):
        cart = get_cart_by_user_id(cart_instance.customer_id)
        if cart:
            cart_id = cart["cart_id"]
            decrement_item_quantity(cart_id, item_id)

    @staticmethod
    def add_item(cart_instance, item_id):
        cart = get_cart_by_user_id(cart_instance.customer_id)
        if cart:
            cart_id = cart["cart_id"]
            increment_item_quantity(cart_id, item_id)

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