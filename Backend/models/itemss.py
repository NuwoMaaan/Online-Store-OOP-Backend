from pydantic import BaseModel

class Item(BaseModel):
    item_id: int
    name: str
    price: float
    
 

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self):
        return self.model_dump()