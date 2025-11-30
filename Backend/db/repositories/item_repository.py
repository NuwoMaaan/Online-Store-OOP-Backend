from db.connection.helper import get_cursor

def create_item(item_data: dict) -> int | None:
    with get_cursor() as cur:
        sql = """
        INSERT INTO item (name, price, quantity)
        VALUES (%s, %s, %s)
        """
        values = (item_data["name"], item_data["price"], item_data["quantity"])
        try:
            cur.execute(sql, values)
            return cur.lastrowid 
        except Exception as e:
            print(f"Error creating item: {e}")
            return None

def get_item_by_id(item_id: int) -> dict | None:
    with get_cursor() as cur:
        sql = "SELECT name, price, quantity FROM item WHERE id = %s"
        cur.execute(sql, (item_id,))
        item = cur.fetchone()
        return item

def get_all_items() -> list[dict]:
    with get_cursor() as cur:
        sql = "SELECT id, name, price FROM item"
        cur.execute(sql)
        items = cur.fetchall()
        return items

