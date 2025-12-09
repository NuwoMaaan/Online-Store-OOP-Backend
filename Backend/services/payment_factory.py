from models.PAYMENT.CardPaymentMethod import CardPaymentMethod
from models.PAYMENT.PaypalPaymentMethod import PaypalPaymentMethod, email_valid


class PaymentFactory:
    @staticmethod
    def create_payment_factory(order):
        factories = {
            "card": CardPaymentMethod(),
            "paypal": PaypalPaymentMethod(),
        }
        while True:
            method = input("\nEnter payment method (card/paypal): ").strip().lower()
            if method in factories:
                factory = factories[method]
                break
            print("Invalid method. Please choose 'card' or 'paypal'.")
        
        if isinstance(factory, CardPaymentMethod):
            print("\n---- Card Payment Method ----:")
            print(" - Card No. length must be 13, 15, or 16 digits")
            print(" - Expiry date format must be MM/YY")
        if isinstance(factory, PaypalPaymentMethod):
            print("\n---- PayPal Payment Method ----:")
            print(f"- Accepted email: {', '.join(email_valid)}")

        kwargs = {}
        for field in factory.get_fields():
            if field == "amount":
                kwargs[field] = order.total
            else:
                kwargs[field] = input(f"Enter {field.replace('_', ' ')}: ")
                
        return factory, kwargs

    @staticmethod
    def process_payment(factory, kwargs):
        try:
            payment = factory.create_payment(**kwargs)
            payment.process()
            return payment
        except ValueError as e:
            print(f"Payment failed: {e}")
            return None
    

    