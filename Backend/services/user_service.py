from models.user import Customer, Staff
import json
import hashlib
import getpass
from db.repositories.user_repository import create_user, get_user_by_username
from db.repositories.cart_repository import create_cart

class UserService():
    @staticmethod
    def check_instance(user) -> bool | None:
        if user is None:
            print("Login failed. Please try again.")
        else:
            if isinstance(user, Customer):
                user.cart.load_cart()
                return True
            elif isinstance(user, Staff):
                print("Logged in as Staff.")
                return False
            else:
                print("Unknown user type.")
            return None
        
    @staticmethod
    def login() -> Customer | Staff | None:
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")

        user = get_user_by_username(username)
        if user is not None and UserService.verify_password(user["password"], password):
            print(f"Login successful. Welcome, {username}!")
            if user["role"] == "customer":
                return Customer(**user)
            elif user["role"] == "staff":
                return Staff(**user)
            else:
                print(f"Unknown role: '{user['role']}' for user {username}")
                return None
        print("Login failed. username or password incorrect.")
        return None

    @staticmethod
    def create_new_user() -> dict | None:
        print("======NEW CUSTOMER ACCOUNT CREATION======")
        email = input("Enter email: ")
        username = input("Enter username: ")
        password = UserService.hash_password(input("Enter password: "))
        confirm = input("Enter 'c' to proceed, 'q' to abort: ").strip().lower()
        if confirm == 'q':
            return print("User creation p rocesses aborted.")
        elif confirm == 'c':
            if '@' in email:
                if get_user_by_username(username) is not None:
                    print("Username already exists.")
                    return None
                new_user = {"username": username,
                            "email": email,
                            "role": "customer",
                            "password": password}
                new_id = create_user(new_user)
                if new_id:
                    print(f"Account created for: {username}")
                    create_cart(new_id)
                    return new_id
            if '@' not in email:
                print("Invalid email. Must contain '@'")
                return None
        else:
            return None
        
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
    
    @staticmethod
    def verify_password(password: str, input: str) -> bool:
        return password == UserService.hash_password(input)