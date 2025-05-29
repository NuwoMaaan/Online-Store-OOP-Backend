from models.cart import Cart
from models.order import Order
from typing import List

class User:
    def __init__(self, user_id: int, username: str, password: str, email: str, role: str):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.email = email
    
    def get_user(self):
        return self.user_id

class Customer(User):
    def __init__(self, user_id: int, username: str, password: str, email: str, role: str = "customer"):
        super().__init__(user_id, username, email, role, password)
        self.cart = Cart(user_id)
        self.orders = []  # List of Order objects

    

class Staff(User):
    def __init__(self, user_id: int, username: str, password: str, email: str, role: str = "staff"):
        super().__init__(user_id, username, email, role, password)