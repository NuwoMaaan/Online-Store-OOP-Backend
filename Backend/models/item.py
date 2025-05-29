<<<<<<< Updated upstream

from pydantic import BaseModel

class Item(BaseModel):
    item_id: str
    name: str
    description: str
    price : float
    stock: int
    category: str

    def is_in_stock(self) -> bool:
        return self.stock > 0

    def reduce_stock(self, quantity: int):
        if quantity <= self.stock:
            self.stock -= quantity
        else:
            raise ValueError("Insufficient stock.")

    def to_dict(self):
        return self.model_dump
=======
from pydantic import BaseModel

class Item(BaseModel):
    item_id: int
    name: str
    price: float
    
 
>>>>>>> Stashed changes

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
<<<<<<< Updated upstream
=======

    def to_dict(self):
        return self.model_dump()
>>>>>>> Stashed changes
