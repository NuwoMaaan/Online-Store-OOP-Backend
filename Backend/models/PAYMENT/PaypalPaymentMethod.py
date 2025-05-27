from PaymentMethod import PaymentMethod
from PaypalPayment import PaypalPayment

email_valid = ['@gmail.com','@yahoo.com','@hotmail.com', '@outlook.com', '@icloud.com']

class PaypalPaymentMethod(PaymentMethod):
    def __init__(self):
        pass

    def get_fields(self):
        return ["amount", "email"]

    def create_payment(self, amount, email) -> PaypalPayment:
        if not any(email.endswith(domain) for domain in email_valid):
            raise ValueError(f"Email must end with one of the following: {', '.join(email_valid)}")
        if "@" not in email:
            raise ValueError("Invalid email format.")
        return PaypalPayment(float(amount), email)

