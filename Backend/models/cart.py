from typing import List
from models.item import Item
from models.order import Order
from services import terminal_payment_service as payment_service
from models.format_items_table import print_items_table

class Cart:
    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        self.items: List[Item] = []
        self.quantity = len(self.items)

    def add_item(self, item: Item):
        self.items.append(item)
        self.quantity = len(self.items)

    def remove_item(self, item_id: int):
        self.items = [item for item in self.items if item.item_id != item_id]
        self.quantity = len(self.items)

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
        

    def checkout(self):
        if not self.items:
            print("Cart it empty. Add Items first before checkout.")
            return None
        self.view_cart()
        print(f"Subtotal: {self.get_total():2f}")
        shipping_details = self.get_shipping_details()
        order = Order(self.customer_id, self.items.copy(), shipping_details)
        self.items: List[Item] = []  # Clear cart after checkout
        return order
    
    def view_cart(self):
        if not self.items:
            print("Your cart is empty.")
            return
        print(f"\nItems in your cart {self.quantity}:")
        print_items_table(self.items)

    @staticmethod
    def cart_menu(user):
        while True:
            user.cart.view_cart()
            menu_choice = input("Enter 'r' to remove an item or 'c' to checkout (or 'q' to quit): ").strip().lower()
            if menu_choice == 'r':
                item_id = input("Enter item ID to remove: ").strip()
                try:
                    item_id = int(item_id)
                    user.cart.remove_item(item_id)
                    print(f"Removed item with ID {item_id} from your cart.")
                except ValueError:
                    print("Invalid item ID. Please enter a valid number.")
            elif menu_choice == 'c':
                payment_service.transaction_procedure(user)
                break
            elif menu_choice == 'q':
                break
            else:
                print("Invalid option. Try again.")