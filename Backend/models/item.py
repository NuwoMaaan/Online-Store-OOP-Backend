# from pydantic import BaseModel

# class Item(BaseModel):
#     item_id: int
#     name: str
#     price: float

class Item():
    def __init__(self, item_id, name, price):
        self.item_id = item_id
        self.name = name
        self.price = price
