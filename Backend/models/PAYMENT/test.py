from CardPaymentMethod import CardPaymentMethod
from PaypalPaymentMethod import PaypalPaymentMethod

def main():
    #card_method = CardPaymentMethod(amount=150.0, card_holder="Alice Smith", card_number="8908002359381788", expiry_date="12/25")
    #paypal_method = PaypalPaymentMethod(amount=150.0, email="leo@outlook.com")

    factory = read_factory()
    user_inputs = get_user_input(factory)

    try:
        factory.process_payment(**user_inputs)
    except ValueError as e:
        print(f"Error processing payment: {e}")

def get_user_input(factory):
    kwargs = {}
    for field in factory.get_fields():
        value = input(f"Enter {field.replace('_', ' ')}: ")
        kwargs[field] = value
    return kwargs

def read_factory():
    """Constructs an Payment Method factory based on the user's preference."""
    factories = {
        "card": CardPaymentMethod(),
        "paypal": PaypalPaymentMethod(),
    }
    while True:
        method = input("Enter payment method (card/paypal): ").strip().lower()
        if method in factories:
            return factories[method]
        print(f"Invalid payment method: {method} Please choose 'card' or 'paypal'.")
        
   

if __name__ == "__main__":
    main()
