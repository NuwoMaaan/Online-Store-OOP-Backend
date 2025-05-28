from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, id: int, name: str, email: str, password: str, address: str, is_admin: bool = False):
        self.id = id
        self.name = name
        self.email = email
        self.password = password  
        self.address = address
        self.is_admin = is_admin

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def from_dict(self, data):
        pass

    @abstractmethod
    def check_password(self, password: str) -> bool:
        pass