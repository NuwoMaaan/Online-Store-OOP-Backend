from abc import ABC, abstractmethod
from Payment import IPayment

class PaymentMethod(ABC):
    @abstractmethod
    def create_payment(self) -> IPayment:
        pass

    def process_payment(self, **kwargs):
        payment = self.create_payment(**kwargs)
        payment.pay()

  
