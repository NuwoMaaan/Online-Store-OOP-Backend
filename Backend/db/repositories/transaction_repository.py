from __future__ import annotations
from db.models import Orders, OrderItems, Item
from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.order import Order

def insert_order(order: Order, db) -> int:
    new_order = Orders(
        user_id=order.customer_id,
        total=order.total,
        date=order.date_time,
        address=order.shipping_details['address'],
        city=order.shipping_details['city'],
        postal_code=order.shipping_details['postal_code']
    )
    db.add(new_order)
    db.flush()
    return new_order.order_id


def insert_order_items(order_id: int, items: list, db) -> int:
    counter = Counter(item.id for item in items)
    for item_id, quantity in counter.items():
        item_obj = next(item for item in items if item.id == item_id)
        item_price = item_obj.price
        line_total = item_price * quantity
        
        order_item = OrderItems(
            order_id=order_id,
            item_id=item_id,
            quantity=quantity,
            price_each=item_price,
            line_total=line_total
        )
        
        db.add(order_item)
        db.flush()
    return order_item.order_id
    

def reduce_stock(order: Order, db) -> bool:
    counter = Counter(item.id for item in order.items)

    for item_id, requested_qty in counter.items():
        item = (db.query(Item).filter(Item.id == item_id).with_for_update().first())
        if not item:
            print(f"Warning: Item {item_id} does not exist.")
            continue

        if item.quantity >= requested_qty:
            item.quantity -= requested_qty
            continue
        # insufficient stock
        print(
            f"Insufficient stock for {item.name}. "
            f"Requested {requested_qty}, available {item.quantity}"
        )
        choice = input("Continue with available stock? (y/n): ").lower().strip()
        if choice != "y":
            return False
        # adjust order and deduct remaining stock
        remove_excess(order, item_id, requested_qty - item.quantity)
        item.quantity = 0
    return True
        

def remove_excess(order: Order, item_id: int, excess: int) -> None:
    removed = 0
    for o_item in list(order.items): 
        if removed >= excess:
            break

        if o_item.id == item_id:
            order.items.remove(o_item)
            removed += 1
    print(f"Removed {removed} items from order.")
