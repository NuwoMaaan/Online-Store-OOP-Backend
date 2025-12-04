from db.repositories.cart_repository import (
    get_cart_by_user_id, 
    decrement_item_quantity, 
    increment_item_quantity, 
    remove_all_items,
    load_cart_db
    )
from models.catalogue import Catalogue


class CartService():
    @staticmethod
    def clear_cart(cart_instance):
        cart = get_cart_by_user_id(cart_instance.customer_id)
        if cart:
            cart_id = cart["cart_id"]
            remove_all_items(cart_id)
    
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
        cart = get_cart_by_user_id(cart_instance.customer_id)
        if cart:
            cart_id = cart["cart_id"]
            cart_items = load_cart_db(cart_id)
            if cart_items:
                catalogue = Catalogue.get_instance() 
                for item in cart_items:
                    item_obj = catalogue.get_item_by_id(int(item["item_id"]))
                    for _ in range(item["quantity"]):
                        if item_obj:
                            cart_instance.items.append(item_obj)
                cart_instance.quantity = len(cart_instance.items)


    
