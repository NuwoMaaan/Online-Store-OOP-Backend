from PaymentMethod import PaymentMethod
from CardPayment import CardPayment

class CardPaymentMethod(PaymentMethod):
    def __init__(self):
        pass

    def create_payment(self, amount, card_holder, card_number, expiry_date) -> CardPayment:
        if not card_number.isdigit() or len(card_number) not in [13, 15, 16]:
            raise ValueError("Invalid card number. Must be numeric and 13-16 digits.")
        if len(expiry_date) != 5 or expiry_date[2] != '/':
            raise ValueError("Invalid expiry date format. Use MM/YY.")
        if float(amount) <= 0:
            raise ValueError("Amount must be positive.")
        return CardPayment(float(amount), card_holder, card_number, expiry_date)
    
    def get_fields(self):
        return ["amount", "card_holder", "card_number", "expiry_date"]
    
    