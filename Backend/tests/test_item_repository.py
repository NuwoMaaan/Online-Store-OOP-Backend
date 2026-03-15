from db.models import Item
from db.repositories.item_repository import create_item, remove_item_catalogue, get_all_items_db
from decimal import Decimal

def test_create_item(db_session):
    item_id = create_item("Test Item", 9.99, 10, db_session)
    assert item_id is not None
    item = db_session.query(Item).filter_by(id=item_id).first()
    assert isinstance(item, Item)
    assert item.name == "Test Item"
    assert item.price == Decimal("9.99")
    assert item.quantity == 10

def test_remove_item_catalogue(db_session):
    item_id = create_item("Test Item", 9.99, 10, db_session)
    result = remove_item_catalogue(item_id, db_session)
    items = db_session.query(Item).filter(Item.quantity > 0).all()
    assert result is True
    assert len(items) == 1 # The item should still exist but with quantity 0
    item = db_session.query(Item).filter_by(id=item_id).first()
    assert item.quantity == 0

def test_get_all_items_db(db_session):
    _ = create_item("Test Item 1", 9.99, 3, db_session)
    _ = create_item("Test Item 2", 15.00, 5, db_session)
    items = get_all_items_db(db_session)
    assert isinstance(items, list)
    assert all(isinstance(item, Item) for item in items)
