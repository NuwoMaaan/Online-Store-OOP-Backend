from abc import ABC, abstractmethod

class IPayment(ABC):
    
    def process(self) -> None:
        self.validate()
        self.pay()
        self.create_salesdocument

    @abstractmethod
    def validate(self) -> None:
        pass

    @abstractmethod
    def pay(self) -> None:
        pass

    def create_salesdocument(self) -> None:
        pass
