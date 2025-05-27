from Payment import IPayment

class CardPayment(IPayment):
    def __init__(self, amount: float, card_holder: str, card_number: str, expiry_date: str):
        self.amount = amount
        self.card_holder = card_holder
        self.card_number = card_number
        self.expiry_date = expiry_date

    #override 
    def pay(self) -> None:
        print(f"Processing card payment of ${self.amount:.2f} for {self.card_holder}, "
              f"card ending in {self.card_number[-4:]}, expires {self.expiry_date}.")
        #payment processing logic would go here
