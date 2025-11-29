
from Backend.db.connection.helper import get_cursor

def create_user(user_data: dict) -> int | None:
    with get_cursor() as cur:
        sql = """
        INSERT INTO users (username, password, email, role)
        VALUES (%s, %s, %s, %s)
        """
        values = (user_data["username"], user_data["password"], user_data["email"], user_data["role"])
        try:
            cur.execute(sql, values)
            return cur.lastrowid # Return the new user's ID
        except Exception as e:
            print(f"Error creating user: {e}")
            return None