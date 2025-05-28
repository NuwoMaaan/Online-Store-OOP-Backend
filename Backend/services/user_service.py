import json
from models.user import User

class UserService:
    def __init__(self, db_path="db/user_data.json"):
        self.db_path = db_path
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.db_path, "r") as f:
                data = json.load(f)
                return [User.from_dict(u) for u in data.get("users", [])]
        except FileNotFoundError:
            return []

    def save_users(self):
        with open(self.db_path, "w") as f:
            json.dump({"users": [u.to_dict() for u in self.users]}, f, indent=4)

    def register(self, user: User):
        if any(u.email == user.email for u in self.users):
            raise ValueError("User with this email already exists.")
        self.users.append(user)
        self.save_users()
        return user

    def login(self, email: str, password: str):
        for user in self.users:
            if user.email == email and user.check_password(password):
                return user
        raise ValueError("Invalid email or password.")
