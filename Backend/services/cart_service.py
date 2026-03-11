from db.repositories.cart_repository import (
    get_cart_by_user_id, 
    decrement_item_quantity, 
    increment_item_quantity, 
    remove_all_items,
    load_cart_db
    )
from models.catalogue import Catalogue
from db.connection.session import get_session


class CartService():
    @staticmethod
    def clear_cart(cart_instance):
        with get_session() as db:
            cart = get_cart_by_user_id(cart_instance.customer_id, db)
            if cart:
                remove_all_items(cart.cart_id, db)
    
    @staticmethod
    def remove_item(cart_instance, item_id):
        with get_session() as db:
            cart = get_cart_by_user_id(cart_instance.customer_id, db)
            if cart:
                decrement_item_quantity(cart.cart_id, item_id, db)

    @staticmethod
    def add_item(cart_instance, item_id):
        with get_session() as db:
            cart = get_cart_by_user_id(cart_instance.customer_id, db)
            if cart:
                increment_item_quantity(cart.cart_id, item_id, db)

    @staticmethod
    def load_cart(cart_instance):
        with get_session() as db:
            cart = get_cart_by_user_id(cart_instance.customer_id, db)
            if cart:
                cart_items = load_cart_db(cart.cart_id)
                if cart_items:
                    catalogue = Catalogue.get_instance() 
                    for item in cart_items:
                        item_obj = catalogue.get_item_by_id(item.item_id)
                        if item_obj:
                            cart_instance.items.extend([item_obj] * item.quantity)
                            
                    cart_instance.quantity = len(cart_instance.items)


    
