from CardPaymentMethod import CardPaymentMethod
from PaypalPaymentMethod import PaypalPaymentMethod

def main():
    print("=== Card Payment ===")
    card_method = CardPaymentMethod(amount=150.0, card_holder="Alice Smith", card_number="8908002359381788", expiry_date="12/25")
    try:
        card_method.process_payment()
    except ValueError as e:
        print(f"Card payment0 error: {e}")

    card_method_invalid = CardPaymentMethod(amount=-4.2, card_holder="#@kke", card_number="123e4", expiry_date="")
    try:
        card_method_invalid.process_payment()
    except ValueError as e:
        print(f"Card payment1 error: {e}")

    print()

    print("=== PayPal Payment ===")
    paypal_method = PaypalPaymentMethod(amount=75.0, email="alice@example.com")
    try:
        paypal_method.process_payment()
    except ValueError as e:
        print(f"PayPal payment0 error: {e}")
    paypal_method_invalid = PaypalPaymentMethod(amount=0, email="invalid-email")
    try:
        paypal_method_invalid.process_payment()
    except ValueError as e:
        print(f"PayPal payment1 error: {e}")

if __name__ == "__main__":
    main()
