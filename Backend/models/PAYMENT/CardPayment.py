from models.PAYMENT.Payment import IPayment
from datetime import datetime

class CardPayment(IPayment):
    def __init__(self, amount: float, card_holder: str, card_number: str, expiry_date: str):
        self.amount = amount
        self.card_holder = card_holder
        self.card_number = card_number
        self.expiry_date = expiry_date

    #validate business logic
    def validate(self) -> None:
        if self.amount <= 0:
            raise ValueError("Amount must be positive.")
        if not self.card_number.isdigit() or len(self.card_number) not in [13, 15, 16]:
            raise ValueError("Invalid card number.")
        if self.is_expired():
            raise ValueError("Card is expired.")

    def is_expired(self) -> bool:
        try:
            exp = datetime.strptime(self.expiry_date, "%m/%y")
            return exp < datetime.now().replace(day=1)
        except ValueError:
            raise ValueError("Invalid expiry date format. Use MM/YY.")

    def pay(self) -> None:
        print(f"Charging ${self.amount:.2f} to card ending in {self.card_number[-4:]}.\n")
    
    # def create_salesdocument(self):
    #     pass
