from typing import List
from models.item import Item
from models.order import Order
from services import payment_service as PaymentService
from utlities.format_items_table import print_items_table
from models.catalogue import Catalogue
import json
import os
from services.cart_service import CartService

cart_db_file = "Backend\db\cart_data.json"

class Cart:
    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        self.items: List[Item] = []
        self.quantity = len(self.items)

    def add_item(self, item: Item):
        self.items.append(item)
        self.quantity = len(self.items)
        CartService.save_cart(self)

    def remove_item(self, item_num_in_cart: int):
        #self.items = [item for item in self.items if item.item_id != item_id]
        self.items.pop(item_num_in_cart)
        self.quantity = len(self.items)
        CartService.save_cart(self)

    def get_total(self):
        return sum(item.price for item in self.items)
    
    def clear_cart_payment(self):
        return CartService.clear_cart_payment(self)
    # def clear_cart_payment(self):
    #     with open(cart_db_file, 'r') as f:
    #         data = json.load(f)
    #     carts = data.get("carts", [])
    #     carts = [cart for cart in carts if cart["customer_id"] != self.customer_id]
    #     carts.clear()
    #     data["carts"] = carts
    #     with open(cart_db_file, "w") as f:
    #         json.dump(data, f, indent=4)


    # def save_cart(self):
    #     if os.path.exists(cart_db_file):
    #         with open(cart_db_file, "r") as f:
    #             data = json.load(f)
    #     else:
    #         data = {"carts": []}
    #     carts = data.get("carts", [])
    #     carts = [cart for cart in carts if cart["customer_id"] != self.customer_id]
    #     carts.append({
    #         "customer_id": self.customer_id,
    #         "items": [{"item_id": str(item.item_id)} for item in self.items]
    #     })
    #     data["carts"] = carts
    #     with open(cart_db_file, "w") as f:
    #         json.dump(data, f, indent=4)


    # def load_cart(self):
    #     with open(cart_db_file, "r") as f:
    #         data = json.load(f)
    #         carts = data.get("carts", [])
    #         user_cart = next((cart for cart in carts if cart["customer_id"] == self.customer_id), None)
    #         if user_cart:
    #             catalogue = Catalogue.get_instance()
    #             self.items = []
    #             for item in user_cart["items"]:
    #                 item_obj = catalogue.get_item_by_id(int(item["item_id"]))
    #                 if item_obj:
    #                     self.items.append(item_obj)
    #         else:
    #             self.items = []
            
    
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
        print(f"Subtotal: {self.get_total():.2f}")
        shipping_details = self.get_shipping_details()
        order = Order(self.customer_id, self.items.copy(), shipping_details)
        self.items: List[Item] = []  # Clear cart after checkout - POTENTIAL ISSUE: customer checkout failure, removes cart before with order process.
        return order
    
    def view_cart(self):
        if not self.items:
            print("Your cart is empty.")
            return
        print(f"\nItems in your cart {self.quantity}:")
        #print_items_table(self.items)
        print(f"{'No.':<4} {'Name':<20} {'Price':>8}")
        for idx, item in enumerate(self.items, 1):
            print(f"{idx:<4} {item.name:<20} ${item.price:>7.2f}")

    @staticmethod
    def cart_menu(user):
        while True:
            user.cart.view_cart()
            menu_choice = input("Enter 'r' to remove an item, 'c' to checkout, or 'q' to quit: ").strip().lower()
            if menu_choice == 'r':
                item_num = input("Enter item number to remove: ").strip()
                try:
                    item_num = int(item_num)
                    if 1 <= item_num <= len(user.cart.items):
                        item_to_remove = user.cart.items[item_num - 1]
                        user.cart.remove_item(item_num - 1)
                        user.cart.quantity = len(user.cart.items)
                        print(f"Removed {item_to_remove.name} from your cart.")
                    else:
                        print("Invalid item number.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            elif menu_choice == 'c':
                PaymentService.transaction_procedure(user)
                break
            elif menu_choice == 'q':
                break
            else:
                print("Invalid option. Try again.")
    
  
   