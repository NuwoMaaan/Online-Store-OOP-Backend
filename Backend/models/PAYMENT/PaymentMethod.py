from abc import ABC, abstractmethod
from Payment import IPayment

class PaymentMethod(ABC):
    @abstractmethod
    def create_payment(self) -> IPayment:
        pass

    @abstractmethod
    def validate(self) -> None:
        pass

    def process_payment(self) -> None:
        payment = self.create_payment()
        self.validate()
        payment.pay()

  
