from db.connection.session import get_session
from db.models import User

def create_user(user_data: dict) -> int:
    with get_session() as db:
        new_user = User(**user_data)
        db.add(new_user)
        db.flush() 
        return new_user.user_id


def get_user_by_username(username: str) -> User | None:
    with get_session() as db:
        user = db.query(User).filter(User.username == username).first()
        return user
        
# def get_user_by_username(username: str) -> dict | None:
#     with get_cursor() as cur:
#         sql = "SELECT user_id, username, password, email, role FROM user WHERE username = %s"
#         cur.execute(sql, (username,))
#         user = cur.fetchone()
#         return user

