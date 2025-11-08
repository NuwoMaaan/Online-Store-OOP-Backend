from models.PAYMENT.Payment import IPayment

class PaypalPayment(IPayment):
    def __init__(self, amount: float, email: str):
        self.amount = amount
        self.email = email

    
    def validate(self) -> None:
        if self.amount <= 0:
            raise ValueError("Amount must be positive.")
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email address.")
        
    def pay(self) -> None:
        print(f"Processing PayPal payment of ${self.amount:.2f} from account {self.email}.\n")

    # def create_salesdocument(self):
    #     pass
