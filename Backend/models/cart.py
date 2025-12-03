from typing import List
from models.item import Item
from models.order import Order
from services.cart_service import CartService
from services.transaction_facade import TransactionFacade 
from services.order_service import OrderService 
from services.payment_service import PaymentService
from services.sales_service import SalesService
from services.cart_service import CartService

transaction = TransactionFacade(OrderService(), PaymentService(), SalesService(), CartService())

class Cart:
    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        self.items: List[Item] = []
        self.quantity = len(self.items)

    def add_item(self, item: Item):
        self.items.append(item)
        self.quantity = len(self.items)
        CartService.add_item(self, item.id)

    def remove_item(self, item_num_in_cart: int, item: Item):
        self.items.pop(item_num_in_cart)
        self.quantity = len(self.items)
        CartService.remove_item(self, item.id)

    def get_total(self):
        return sum(item.price for item in self.items)
    
    def clear_cart(self):
        self.items = []
        return CartService.clear_cart(self)
       
    def get_shipping_details(self) -> dict:
        address = input("Enter shipping address: ")
        city = input("Enter city: ")
        postal_code = input("Enter postal code: ")
        return {
            "address": address,
            "city": city,
            "postal_code": postal_code
        }
        
    def checkout(self) -> Order:
        if not self.items:
            print("Cart it empty. Add Items first before checkout.")
            return None
        self.view_cart()
        print(f"Subtotal: {self.get_total():.2f}")
        shipping_details = self.get_shipping_details()
        order = Order(self.customer_id, self.items.copy(), shipping_details)
        #self.items: List[Item] = []  # Clear cart after checkout - POTENTIAL ISSUE: customer checkout failure, removes cart before with order process.
        return order
    
    def view_cart(self):
        if not self.items:
            print("Your cart is empty.")
            return
        print(f"\nItems in your cart {self.quantity}:")
        print(f"{'No.':<4} {'Name':<20} {'Price':>8}")
        for idx, item in enumerate(self.items, 1):
            print(f"{idx:<4} {item.name:<20} ${item.price:>7.2f}")

    @staticmethod
    def cart_menu(user):
        while True:
            user.cart.view_cart()
            menu_choice = input("Enter 'r' to remove an item, 'c' to checkout, or 'q' to quit: ").strip().lower()
            if menu_choice == 'r':
                item_num = int(input("Enter item number to remove: ").strip()) - 1 # Adjust for 0-based index
                try:
                    if 0 <= item_num <= len(user.cart.items):
                        item = user.cart.items[item_num]
                        user.cart.remove_item(item_num, item)
                        print(f"Removed {item.name} from your cart.")
                    else:
                        print("Invalid item number.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            elif menu_choice == 'c':
                transaction.process(user)
                break
            elif menu_choice == 'q':
                break
            else:
                print("Invalid option. Try again.")
    
  
   