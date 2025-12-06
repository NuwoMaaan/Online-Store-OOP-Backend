from db.connection.helper import get_cursor
from collections import Counter

def insert_order(order):
    with get_cursor() as cur:
        sql = "INSERT INTO orders (user_id, total, date, address, city, postal_code)" \
        " VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (order.customer_id,
                          order.total, 
                          order.date_time,
                          order.shipping_details["address"],
                          order.shipping_details["city"],
                          order.shipping_details["postal_code"]))
        return cur.lastrowid 
 
def insert_order_items(order_id, items):
    with get_cursor() as cur:
        sql = "INSERT INTO order_items (order_id, item_id, quantity, price_each, line_total)" \
        " VALUES (%s, %s, %s, %s, %s)"
        counter = Counter(item.id for item in items)

        for item_id, quantity in counter.items():
            item_price = next(item.price for item in items if item.id == item_id)
            line_total = item_price * quantity
        
            cur.execute(sql, (order_id, item_id, quantity, item_price, line_total))

def reduce_stock(order):
    with get_cursor() as cur:
        counter = Counter(item.id for item in order.items)

        for item_id, quantity_needed in counter.items():
            sql_select = "SELECT quantity FROM item WHERE id = %s FOR UPDATE"
            cur.execute(sql_select, (item_id,))
            row = cur.fetchone()
            if not row:
                print(f"Warning: Item {item_id} does not exist.")
                continue
            current_quantity = row["quantity"]

            if current_quantity < quantity_needed:
                print(
                    f"Insufficient stock for item {item_id}. Requested {quantity_needed}, "
                    f"available {current_quantity}."
                )
                choice = input("y/n - Continue with available items (y) or exit (n): ").lower().strip()
                if choice == "y":
                    # Remove the excess items from order.items 
                    excess = quantity_needed - current_quantity
                    removed = 0  
                    for item in list(order.items):
                        if removed >= excess:
                            break
                        if item.id == item_id:
                            order.items.remove(item)
                            removed += 1
                    # Adjust quantity_needed to what's available
                    quantity_needed = current_quantity
                    print(f"Proceeding with {quantity_needed} of item {item_id} (removed {removed} items).")
                else:
                    print("Terminating transaction - Returning to menu")
                    return False
                    
            sql_update = "UPDATE item SET quantity = quantity - %s WHERE id = %s"
            cur.execute(sql_update, (quantity_needed, item_id))
    return True
