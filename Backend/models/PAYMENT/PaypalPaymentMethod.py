from PaymentMethod import PaymentMethod
from PaypalPayment import PaypalPayment

class PaypalPaymentMethod(PaymentMethod):
    def __init__(self):
        pass
        
    def create_payment(self, amount, email) -> PaypalPayment:
        if not email or "@" not in email:
            raise ValueError("Invalid email address.")
        if float(amount) <= 0:
            raise ValueError("Amount must be positive.")
        return PaypalPayment(float(amount), email)

    
    def get_fields(self):
        return ["amount", "email"]

    # #override
    # def validate(self) -> None:
    #     if not self.email or "@" not in self.email:
    #         raise ValueError("Invalid email address for PayPal payment.")
    #     if self.amount <= 0:
    #         raise ValueError("Payment amount must be greater than zero.")
    