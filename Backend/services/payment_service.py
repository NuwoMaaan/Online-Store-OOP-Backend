from services.payment_factory import PaymentFactory

class PaymentService:
    @staticmethod
    def process(order):
        factory, kwargs = PaymentFactory.create_payment_factory(order)
        return PaymentFactory.process_payment(factory, kwargs)