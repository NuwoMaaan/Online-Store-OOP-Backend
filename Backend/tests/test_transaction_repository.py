from db.models import Orders, OrderItems
from models.order import Order
from models.item import Item
from db.repositories.transaction_repository import insert_order, insert_order_items, reduce_stock
from decimal import Decimal


item = Item(id=1, name="Test Item", price=10.00)
order_data = Order(
        customer_id=1,
        items=[item, item],
        shipping_details={
            "address": "123 Test St",
            "city": "Testville",
            "postal_code": "3000"
        }
    )

def test_insert_order(db_session):
    order_id = insert_order(order_data, db_session)
    assert isinstance(order_id, int)
    
    order = db_session.query(Orders).filter_by(order_id=order_id).first()
    assert order is not None
    assert order.user_id == 1
    assert order.total == Decimal("30.00")  # shipping + item price
    assert order.address == "123 Test St"
    assert order.city == "Testville"
    assert order.postal_code == "3000"

def test_insert_order_items(db_session):
    order_id = insert_order(order_data, db_session)
    order_item_id = insert_order_items(order_id, order_data.items, db_session)
    assert isinstance(order_item_id, int)

    order_item = db_session.query(OrderItems).filter_by(order_id=order_id).first()
    assert order_item.item_id == 1
    assert order_item.quantity == 2
    assert order_item.price_each == Decimal("10.00")
    assert order_item.line_total == Decimal("20.00")

def reduce_stock(db_session):
    # This test is more complex due to user input.
    # Need to refactor repository to move input out into a separate function for better testability.
    pass

