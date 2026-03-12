from db.models import User


def create_user(user_data: dict, db) -> int:
        new_user = User(
              username=user_data["username"],
              password=user_data["password"],
              role=user_data["role"],
              email=user_data["email"]
        )
        db.add(new_user)
        db.flush() 
        return new_user.user_id


def get_user_by_username(username: str, db) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    return user
        
# def get_user_by_username(username: str) -> dict | None:
#     with get_cursor() as cur:
#         sql = "SELECT user_id, username, password, email, role FROM user WHERE username = %s"
#         cur.execute(sql, (username,))
#         user = cur.fetchone()
#         return user

