from Backend.db.connection.helper import get_cursor

def list_items():
    with get_cursor() as cur:
        cur.execute("SELECT item_id, name, price FROM items")
        return cur.fetchall()

def get_item(item_id):
    with get_cursor() as cur:
        cur.execute("SELECT item_id, name, price FROM items WHERE item_id = %s", (item_id,))
        return cur.fetchone()