from models.cart import Cart
from abc import ABC


class User(ABC):
    def __init__(self, user_id: int, username: str, password: str, email: str, role: str):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.email = email

    
class Customer(User):
    def __init__(self, user_id: int, username: str, password: str, email: str, role: str = "customer"):
        super().__init__(user_id, username, email, role, password)
        self.cart = Cart(user_id)
        self.orders = []  

class Staff(User):
    def __init__(self, user_id: int, username: str, password: str, email: str, role: str = "staff"):
        super().__init__(user_id, username, email, role, password)      