from models.cart import Cart
from abc import ABC
import json

class User(ABC):
    def __init__(self, user_id: int, username: str, password: str, email: str, role: str):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.email = email
    
    def get_user(self):
        return self.user_id
    
    @staticmethod
    def login():
        username = input("Enter username: ")
        password = input("Enter password: ")
        with open("Backend/db/user_data.json", "r") as f:
            data = json.load(f)
            users = data.get("users", [])
        for user in users:
            if user["username"] == username and user["password"] == password:
                print(f"Login successful. Welcome, {username}!")
                if user["role"] == "customer":
                    return Customer(**user)
                elif user["role"] == "staff":
                    return Staff(**user)
                else:
                    print(f"Unknown role: '{user['role']}' for user {username}")
                    return None
        print("Login failed. Invalid username or password.")
        return None

    @staticmethod
    def create_new_user():
        print("======NEW CUSTOMER ACCOUNT CREATION======")
        email = input("Enter email: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        if '@' in email:
            with open("Backend/db/user_data.json", "r+") as f:
                data = json.load(f)
                users = data.get("users", [])

                existing_ids = {user["user_id"] for user in users}
                new_id = 1
                while new_id in existing_ids:
                    new_id += 1

                for user in users:
                    if user["username"] == username:
                        print("Username already exists.")
                        return None
                    if user["email"] == email:
                        print("Email already registered.")
                        return None
        
                new_user = {"user_id": new_id,"username": username,"email": email,"role": "customer","password": password}
                users.append(new_user)
                data["users"] = users
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            print(f"Account created for: {username}")
            return new_user
        if '@' not in email:
            print("Invalid email. Must contain '@'")
            return None

class Customer(User):
    def __init__(self, user_id: int, username: str, password: str, email: str, role: str = "customer"):
        super().__init__(user_id, username, email, role, password)
        self.cart = Cart(user_id)
        self.orders = []  # List of Order objects

    

class Staff(User):
    def __init__(self, user_id: int, username: str, password: str, email: str, role: str = "staff"):
        super().__init__(user_id, username, email, role, password)