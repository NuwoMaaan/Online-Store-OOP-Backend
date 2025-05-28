

class PaymentService:
    def __init__(self, PaymentMFactory):
        self.PaymentMfactory = PaymentMFactory

    def process_payment(self, data: dict):
        payment = self.PaymentMfactory.create_payment(**data)
        payment.validate()
        payment.pay()