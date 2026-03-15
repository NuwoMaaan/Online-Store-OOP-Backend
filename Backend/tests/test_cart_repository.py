from db.repositories.cart_repository import (
    create_cart,
    get_cart_by_user_id, 
    remove_all_items, decrement_item_quantity, 
    increment_item_quantity, load_cart_db
    )
from db.models import Cart, CartItems

def test_create_cart(db_session):
    cart = Cart(user_id=1)
    cart_id = create_cart(cart.user_id, db_session)
    assert cart_id is not None
    assert isinstance(cart_id, int)
    assert cart_id == 1

def test_get_cart_by_user_id(db_session):
    cart = Cart(user_id=1)
    cart_id = create_cart(cart.user_id, db_session)
    cart = get_cart_by_user_id(cart_id, db_session)
    assert cart is not None
    assert isinstance(cart, Cart)
    assert cart.user_id == 1

def test_get_cart_by_user_id_not_found(db_session):
    non_exist_cart_id = 999
    cart = get_cart_by_user_id(non_exist_cart_id, db_session)
    assert cart is None

def test_remove_all_items(db_session):
    cart = Cart(user_id=1)
    cart_id = create_cart(cart.user_id, db_session)
    item1 = CartItems(cart_id=cart_id, item_id=1, quantity=2)
    item2 = CartItems(cart_id=cart_id, item_id=2, quantity=3)
    db_session.add_all([item1, item2])
    db_session.commit()

    remove_all_items(cart_id, db_session)
    items = db_session.query(CartItems).filter_by(cart_id=cart_id).all()
    assert len(items) == 0
    assert items == []
    

def test_decrement_item_quantity(db_session):
    cart = Cart(user_id=1)
    cart_id = create_cart(cart.user_id, db_session)
    item = CartItems(cart_id=cart_id, item_id=1, quantity=3)
    db_session.add(item)
    db_session.commit()

    decrement_item_quantity(cart_id, 1, db_session)
    updated_items = db_session.query(CartItems).filter_by(cart_id=cart_id, item_id=1).all()
    item = updated_items[0]
    assert len(updated_items) == 1
    assert item.quantity == 2


def test_increment_item_quantity_existing_item(db_session):
    cart_id = create_cart(1, db_session)
    item = CartItems(cart_id=cart_id, item_id=1, quantity=2)
    db_session.add(item)
    db_session.commit()

    increment_item_quantity(cart_id, 1, db_session)
    updated_item = db_session.query(CartItems).filter_by(cart_id=cart_id, item_id=1).first()
    assert updated_item.quantity == 3


def test_increment_item_quantity_creates_item(db_session):
    cart_id = create_cart(1, db_session)

    increment_item_quantity(cart_id, 1, db_session)
    new_item = db_session.query(CartItems).filter_by(cart_id=cart_id, item_id=1).first()
    assert new_item.quantity == 1

def test_load_cart_db(db_session):
    cart_id = create_cart(1, db_session)
    item1 = CartItems(cart_id=cart_id, item_id=1, quantity=2)
    item2 = CartItems(cart_id=cart_id, item_id=2, quantity=3)
    db_session.add_all([item1, item2])
    db_session.commit()

    cart_items = load_cart_db(cart_id, db_session)
    item1, item2 = cart_items[0], cart_items[1]
    assert len(cart_items) == 2
    assert item1.item_id == 1
    assert item1.quantity == 2
    assert item2.item_id == 2
    assert item2.quantity == 3