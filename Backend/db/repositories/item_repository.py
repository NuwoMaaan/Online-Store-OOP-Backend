from db.connection.session import get_session
from db.models import Item
from sqlalchemy import update

def create_item(name: str, price: float, quantity: int) -> int | None:
    with get_session() as db:
        new_item = Item(name=name, price=price, quantity=quantity)
        db.add(new_item)
        db.flush() 
        return new_item.id
    

def remove_item_catalogue(item_id: int) -> bool:
    with get_session() as db:
        item = db.query(Item).filter_by(id=item_id).first()
        if item:
            item.quantity = 0
            return True    
        return False
    

def get_all_items_db() -> list[Item]:
    with get_session() as db:
        items = db.query(Item).filter(Item.quantity > 0).all()
        return items

