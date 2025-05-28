from models.PAYMENT.CardPayment import CardPayment
from models.PAYMENT.PaymentMethod import PaymentMethod

class CardPaymentMethod(PaymentMethod):
    def __init__(self):
        pass

    def get_fields(self):
        return ["amount", "card_holder", "card_number", "expiry_date"]

    #validate the input data before creating a payment
    def create_payment(self, amount, card_holder, card_number, expiry_date) -> CardPayment:
        if not card_number.isdigit():
            raise ValueError("Card number must be numeric.")
        if len(expiry_date) != 5 or expiry_date[2] != '/':
            raise ValueError("Invalid expiry date format. Use MM/YY.")
        return CardPayment(float(amount), card_holder, card_number, expiry_date)
