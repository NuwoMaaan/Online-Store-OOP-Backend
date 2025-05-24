from PaymentMethod import PaymentMethod
from CardPayment import CardPayment

class CardPaymentMethod(PaymentMethod):
    def __init__(self, amount: float, card_holder: str, card_number: str, expiry_date: str):
        self.amount = amount
        self.card_holder = card_holder
        self.card_number = card_number
        self.expiry_date = expiry_date

    def create_payment(self) -> CardPayment:
        return CardPayment(self.amount, self.card_holder, self.card_number, self.expiry_date)
    
    #override
    def validate(self):
        if not self.card_holder or not self.card_number or not self.expiry_date:
            raise ValueError("Card holder, card number, and expiry date must be provided.")
        if len(self.card_number) != 16 or not self.card_number.isdigit():
            raise ValueError("Card number must be a 16-digit number.")
        if self.amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        # Additional validation for expiry date can be added here
