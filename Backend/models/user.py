from models.cart import Cart


class User:
    def __init__(self, user_id: int, name: str, email: str, role: str):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.email = email

class Customer(User):
    def __init__(self, user_id: int, name: str, email: str, role: str = "customer"):
        super().__init__(user_id, name, email, role)
        self.cart = Cart(user_id)



class Staff(User):
    def __init__(self, user_id: int, name: str, email: str, role: str = "staff"):
        super().__init__(user_id, name, email, role)