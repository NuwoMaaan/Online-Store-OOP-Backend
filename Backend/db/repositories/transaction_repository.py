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
        