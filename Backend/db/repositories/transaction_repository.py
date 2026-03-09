from db.connection.session import get_session
from models.order import Order
from models import Orders, OrderItems, Item
from collections import Counter

def insert_order(order: Order) -> int:
    with get_session() as db:
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


def insert_order_items(order_id: int, items: list) -> int:
    with get_session() as db:
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
            db.flush
            return order_item.order_id
        

def reduce_stock(order: Order) -> bool:
    with get_session() as db:
        counter = Counter(item.id for item in order.items)
        for item_id, quantity_needed in counter.items():
            # Lock the row for update
            item = db.query(Item).filter_by(id=item_id).with_for_update().first()
            if not item:
                print(f"Warning: Item {item_id} does not exist.")
                continue
            # Stock Check Logic
            if item.quantity < quantity_needed:
                print(f"Insufficient stock for {item.name}. Requested {quantity_needed}, available {item.quantity}.")
                choice = input("y/n - Continue with available items (y) or exit (n): ").lower().strip()
                
                if choice == "y":
                    excess = quantity_needed - item.quantity
                    removed = 0
                    # Modifying the order object item list
                    for o_item in order.items:
                        if removed < excess and o_item.id == item_id:
                            order.items.remove(o_item)
                            removed += 1
                    
                    quantity_needed = item.quantity
                    print(f"Proceeding with {quantity_needed} (removed {removed}).")
                else:
                    print("Terminating transaction - Returning to menu")
                    # Context manager will automatically ROLLBACK because we return False 
                    return False

            # finalise stock reduction
            item.quantity -= quantity_needed
    return True