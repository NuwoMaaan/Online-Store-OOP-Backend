from models.PAYMENT.CardPaymentMethod import CardPaymentMethod
from models.PAYMENT.PaypalPaymentMethod import PaypalPaymentMethod

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

    kwargs = {}
    for field in factory.get_fields():
        if field == "amount":
            kwargs[field] = order.total   
        else:
            kwargs[field] = input(f"Enter {field.replace('_', ' ')}: ")
            
    return factory, kwargs

def process_payment(factory, kwargs):
    try:
        payment = factory.create_payment(**kwargs)
        payment.process()
        # payment.validate()
        # payment.pay()
        return payment
    except ValueError as e:
        print(f"Payment failed: {e}")
        return None