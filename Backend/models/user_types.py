class User:
    def __init__(self, user_id, username, email, role, password=None):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.email = email
        self.password = None

class Customer(User):
    def __init__(self, user_id, username, email, shipping_address=None):
        super().__init__(user_id, username, email, password=None)
        self.shipping_address = shipping_address

    def add_to_cart(self, id, price, quantity=1):
        pass

class Staff(User):
    def __init__(self, user_id, username, email):
        super().__init__(user_id, username, email, password=None)
        