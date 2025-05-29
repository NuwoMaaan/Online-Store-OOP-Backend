from typing import List
from models.item import Item
from models.order import Order

class Cart:
    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        self.items: List[Item] = []

    def add_item(self, item: Item):
        self.items.append(item)

    def remove_item(self, item_id: int):
        self.items = [item for item in self.items if item.item_id != item_id]

    def get_total(self):
        return sum(item.price for item in self.items)

    def get_items(self):
        return self.items
    
    def to_dict(self):
        return [item.to_dict() for item in self.items]
    
    def get_shipping_details(self, address: str, city: str, postal_code: str):
        return {
            "address": address,
            "city": city,
            "postal_code": postal_code
        }
        

    def checkout(self, customer_id, shipping_details):
            total = self.get_total()
            # order = {
            #     "customer_id": self.customer_id,
            #     "items": self.to_dict(),
            #     "total": total
            # }

            
            order = Order(customer_id, shipping_details,)
            self.items = []
            return order