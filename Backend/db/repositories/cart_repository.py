from sqlalchemy import delete
from db.models import Cart, CartItems
from typing import List

def create_cart(user_id: int, db) -> None:
        new_cart = Cart(user_id=user_id)
        db.add(new_cart)


def get_cart_by_user_id(user_id: int, db) -> Cart | None:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        return None
    return cart
    

def remove_all_items(cart_id: int, db) -> None:
    sql = delete(CartItems).where(CartItems.cart_id == cart_id)
    db.execute(sql)


def decrement_item_quantity(cart_id: int, item_id: int, db) -> None:
    item = db.query(CartItems).filter_by(cart_id=cart_id, item_id=item_id).first()
    if not item:
        return

    if item.quantity > 1:
        item.quantity -= 1
    else:
        db.delete(item)


def increment_item_quantity(cart_id: int, item_id: int, db) -> None:
    item = db.query(CartItems).filter_by(cart_id=cart_id, item_id=item_id).first()
    if item:
        item.quantity += 1
    else:
        new_item = CartItems(cart_id=cart_id, item_id=item_id, quantity=1)
        db.add(new_item)


def load_cart_db(cart_id: int, db) -> List[CartItems] | None:
        cart_items = db.query(CartItems.item_id, CartItems.quantity).filter_by(cart_id=cart_id).all()
        return cart_items
        
