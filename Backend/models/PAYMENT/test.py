from CardPaymentMethod import CardPaymentMethod
from PaypalPaymentMethod import PaypalPaymentMethod

def read_factory():
    factories = {
        "card": CardPaymentMethod(),
        "paypal": PaypalPaymentMethod(),
    }
    while True:
        method = input("Enter payment method (card/paypal): ").strip().lower()
        if method in factories:
            return factories[method]
        print("Invalid method. Please choose 'card' or 'paypal'.")

def get_user_input(factory):
    kwargs = {}
    for field in factory.get_fields():
        value = input(f"Enter {field.replace('_', ' ')}: ")
        kwargs[field] = value
    return kwargs

def main():
    factory = read_factory()
    user_inputs = get_user_input(factory)

    try:
        payment = factory.create_payment(**user_inputs)
        payment.validate()            
        payment.pay()     
    except ValueError as e:
        print(f"Payment failed: {e}")

if __name__ == "__main__":
    main()
