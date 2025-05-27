from Payment import IPayment

class PaypalPayment(IPayment):
    def __init__(self, amount: float, email: str):
        self.amount = amount
        self.email = email

    #override
    def pay(self) -> None:
        print(f"Processing PayPal payment of ${self.amount:.2f} from account {self.email}.")
