from PaymentMethod import PaymentMethod
from PaypalPayment import PaypalPayment

class PaypalPaymentMethod(PaymentMethod):
    def __init__(self, amount: float, email: str):
        self.amount = amount
        self.email = email

    def create_payment(self) -> PaypalPayment:
        return PaypalPayment(self.amount, self.email)

    #override
    def validate(self) -> None:
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email address for PayPal payment.")
        if self.amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
    