class CartItem:
    def __init__(self, item_id: str, price: float, quantity: int = 1):
        self.item_id = item_id
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "price": self.price,
            "quantity": self.quantity
        }

    @classmethod
    def from_dict(cls, data):
        try:
            return cls(
                item_id=data["item_id"],
                price=data["price"],
                quantity=data.get("quantity", 1)
            )
        except KeyError as e:
            raise ValueError(f"Missing required key in CartItem data: {e}")
