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
    
    def get_shipping_details(self):
        address = input("Enter shipping address: ")
        city = input("Enter city: ")
        postal_code = input("Enter postal code: ")
        return {
            "address": address,
            "city": city,
            "postal_code": postal_code
        }
        

    def checkout(self, shipping_details):
        order = Order(self.customer_id, self.items.copy(), shipping_details)
        self.items: List[Item] = []  # Clear cart after checkout
        return order
    


    