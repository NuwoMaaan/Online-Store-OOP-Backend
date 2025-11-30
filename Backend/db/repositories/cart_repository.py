from db.connection.helper import get_cursor
from models.item import Item

def create_cart(user_id: int):
    with get_cursor() as cur:
        sql = "INSERT INTO cart (user_id) VALUES (%s)"
        cur.execute(sql, (user_id,))
        #return cur.lastrowid

def get_cart_by_user_id(user_id: int) -> dict | None:
    with get_cursor() as cur:
        sql = "SELECT cart_id, User_id FROM cart WHERE user_id = %s"
        cur.execute(sql, (user_id,))
        cart = cur.fetchone()
        return cart

def delete_cart_by_cart_id(cart_id: int):
    with get_cursor() as cur:
        sql = "DELETE FROM cart_items WHERE user_id = %s"
        cur.execute(sql, (cart_id,))

def save_cart_by_cart_id(cart_id: int, items: list[Item]):
    quantities = {}
    for item in items:
        quantities[item.id] = quantities.get(item.id, 0) + 1

    with get_cursor() as cur:
        sql = """
        INSERT INTO cart_items (cart_id, item_id, quantity)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE quantity = VALUES (quantity)
        """
        item_data_list = [(cart_id, item_id, qty) for item_id, qty in quantities.items()]
        cur.executemany(sql, item_data_list)

def load_cart_by_cart_id(cart_id: int) -> list[Item]:
    with get_cursor() as cur:
        pass
