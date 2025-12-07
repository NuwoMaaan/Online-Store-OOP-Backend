from db.connection.helper import get_cursor

def create_item(name: str, price: float, quantity: int) -> int | None:
    with get_cursor() as cur:
        sql = "INSERT INTO item (name, price, quantity) VALUES (%s, %s, %s)"
        try:
            cur.execute(sql, (name, price, quantity))
            return cur.lastrowid
        except Exception as e:
            print(f"Error creating item: {e}")
            return None

def remove_item_catalogue(item_id: int) -> bool:
    with get_cursor() as cur:
        sql = "UPDATE item SET quantity = 0 WHERE id = %s"
        cur.execute(sql, (item_id,))
        if cur.rowcount > 0:
            return True
        return False


def get_item_by_id(item_id: int) -> dict[str, int] | None:
    with get_cursor() as cur:
        sql = "SELECT name, price, quantity FROM item WHERE id = %s"
        cur.execute(sql, (item_id,))
        item = cur.fetchone()
        return item

def get_all_items_db() -> list[dict[str, int]]:
    with get_cursor() as cur:
        sql = "SELECT id, name, price, quantity FROM item WHERE quantity > 0"
        cur.execute(sql)
        items = cur.fetchall()
        return items

