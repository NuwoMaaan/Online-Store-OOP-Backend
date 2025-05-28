# models/product.py
from pydantic import BaseModel
class Item(BaseModel):

    def __init__(self, id: int, name: str, description: str, price: float, stock: int, category: str):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category = category

    def is_in_stock(self) -> bool:
        return self.stock > 0

    def reduce_stock(self, quantity: int):
        if quantity <= self.stock:
            self.stock -= quantity
        else:
            raise ValueError("Insufficient stock.")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "category": self.category
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            price=data["price"],
            stock=data["stock"],
            category=data["category"]
        )
