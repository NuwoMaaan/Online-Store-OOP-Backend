from db.connection.helper import get_cursor
from models.item import Item

def create_cart(user_id: int):
    with get_cursor() as cur:
        sql = "INSERT INTO cart (user_id) VALUES (%s)"
        cur.execute(sql, (user_id,))
        #return cur.lastrowid

def get_cart_by_user_id(user_id: int) -> dict | None:
    with get_cursor() as cur:
        sql = "SELECT cart_id, user_id FROM cart WHERE user_id = %s"
        cur.execute(sql, (user_id,))
        cart = cur.fetchone()
        return cart

def remove_all_by_cart_id(cart_id: int):
    with get_cursor() as cur:
        sql = "DELETE FROM cart_items WHERE cart_id = %s"
        cur.execute(sql, (cart_id,))

def decrement_item_quantity(cart_id: int, item_id: int):
    with get_cursor() as cur:
        sql = "SELECT quantity FROM cart_items WHERE cart_id = %s AND item_id = %s"
        cur.execute(sql, (cart_id, item_id))
        row = cur.fetchone()
        if not row:
            return
        new_qty = row["quantity"] - 1
        if new_qty > 0:
            sql = "UPDATE cart_items SET quantity = %s WHERE cart_id = %s AND item_id = %s"
            cur.execute(sql, (new_qty, cart_id, item_id))
        else:
            sql = "DELETE FROM cart_items WHERE cart_id = %s AND item_id = %s"
            cur.execute(sql, (cart_id, item_id))

def increment_item_quantity(cart_id: int, item_id: int):
    with get_cursor() as cur:
        sql = "SELECT quantity FROM cart_items WHERE cart_id = %s AND item_id = %s"
        cur.execute(sql, (cart_id, item_id))
        row = cur.fetchone()
        if not row:
            sql = "INSERT INTO cart_items (cart_id, item_id, quantity) VALUES (%s, %s, %s)"
            cur.execute(sql, (cart_id, item_id, 1))
            return
        new_qty = row["quantity"] + 1
        sql = "UPDATE cart_items SET quantity = %s WHERE cart_id = %s AND item_id = %s"
        cur.execute(sql, (new_qty, cart_id, item_id))


def load_cart_by_cart_id(cart_id: int) -> list[Item]:
    with get_cursor() as cur:
        pass
