import pytest
from decimal import Decimal
from db.models import Orders, OrderItems, Item
from models.order import Order
from models.item import Item as DomainItem
from db.repositories.transaction_repository import (
    insert_order,
    insert_order_items, 
    reduce_stock, check_stock, 
    remove_excess
    )
from db.repositories.item_repository import create_item


@pytest.fixture
def test_item():
    return DomainItem(id=1, name="Test Item", price=10.00)

@pytest.fixture
def test_order(test_item):
    return Order(
        customer_id=1,
        items=[test_item, test_item],
        shipping_details={
            "address": "123 Test St",
            "city": "Testville",
            "postal_code": "3000"
        }
    )


def test_insert_order(db_session, test_order):
    order_id = insert_order(test_order, db_session)
    assert isinstance(order_id, int)

    order = db_session.query(Orders).filter_by(order_id=order_id).first()
    assert order is not None
    assert order.user_id == 1
    assert order.total == Decimal("30.00")
    assert order.address == "123 Test St"
    assert order.city == "Testville"
    assert order.postal_code == "3000"


def test_insert_order_items(db_session, test_order):
    order_id = insert_order(test_order, db_session)
    order_item_id = insert_order_items(order_id, test_order.items, db_session)
    assert isinstance(order_item_id, int)

    order_item = db_session.query(OrderItems).filter_by(order_id=order_id).first()
    assert order_item.item_id == 1
    assert order_item.quantity == 2
    assert order_item.price_each == Decimal("10.00")
    assert order_item.line_total == Decimal("20.00")

def test_reduce_stock(db_session, test_order):
    item_name = "Test Item"
    item_price = 10.00
    item_quantity = 100
    
    item_id = create_item(item_name, item_price, item_quantity, db_session)
    success = reduce_stock(test_order, db_session)
    assert success

    item = db_session.query(Item).filter_by(id=item_id).first()
    assert item.quantity == 98 

def test_check_stock_is_short(db_session, test_order): 
    item_name = "Test Item"
    item_price = 10.00
    item_quantity = 1

    _ = create_item(item_name, item_price, item_quantity, db_session)
    shortage = check_stock(test_order, db_session)
    assert len(shortage) == 1
    assert shortage[0]['requested'] == 2
    assert shortage[0]['available'] == 1
    assert shortage[0]['missing'] == 1


def test_check_stock_not_short(db_session, test_order): 
    item_name = "Test Item"
    item_price = 10.00
    item_quantity = 3

    _ = create_item(item_name, item_price, item_quantity, db_session)
    shortage = check_stock(test_order, db_session)
    assert len(shortage) == 0
