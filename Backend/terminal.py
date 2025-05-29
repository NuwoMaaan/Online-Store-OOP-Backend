from models.user import Customer
from models.catalogue import Catalogue
from models.cart import Cart
from models.item import Item
from models.order import Order
from models.PAYMENT import Payment
from models.PAYMENT import CardPayment
from models.PAYMENT import PaypalPayment
from models.PAYMENT import PaymentMethod
from models.PAYMENT import CardPaymentMethod
from models.PAYMENT import PaypalPaymentMethod
import json




def main():
    print("This is the terminal interface for the backend system.")
    print("You can run various commands to interact with the system.")
    
    while True:
        print("\nAvailable commands:")
        print("1 - Login")
        print("2 - Exit")
        command = input("Enter command number: ").strip()
        if command == "2":
            print("Exiting terminal. Goodbye!")
            break
        elif command == "1":
            user = login()
            if user is None:
                print("Login failed. Please try again.")
                menu(user)
        else:
            print(f"Unknown command: {command}")

def menu(user):
    print("\nWelcome to the main menu!")
    print("1 - View Catalogue")
    print("2 - View Cart")
    print("3 - Checkout")
    print("4 - Exit")

    while True:
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            view_catalogue()
        elif choice == "2":
            view_cart(user)
        elif choice == "3":
            checkout()
        elif choice == "4":
            print("Exiting. Goodbye!")
            break
        else:
            print(f"Unknown option: {choice}") 

def view_catalogue():
    catalogue = Catalogue.get_instance()
    items = catalogue.get_all_items()
    if not items:
        print("No items available in the catalogue.")
        return
    print("\nCatalogue Items:")
    for item in items:
        print(f"{item.item_id}: {item.name} - ${item.price:.2f}")

def view_cart(user: Customer):
    cart = user.cart
    if not cart.items:
        print("Your cart is empty.")
        return
    print("\nItems in your cart:")
    for item in cart.items:
        print(f"{item.item_id}: {item.name} - ${item.price:.2f}")

def checkout():
    address = input("Enter shipping address: ")
    city = input("Enter city: ")
    postal_code = input("Enter postal code: ")

    # Assuming you have a way to get the current user's ID
    customer_id = 1  # Replace with actual customer ID logic

    cart = Cart(customer_id)
    shipping_details = cart.get_shipping_details(address, city, postal_code)

    order = cart.checkout(customer_id, shipping_details)
    
    print("\nOrder Summary:")
    print(f"Customer ID: {order.customer_id}")
    for item in order.items:
        print(f"- {item.name}: ${item.price:.2f}")
    print(f"Total: ${order.total:.2f}")
    

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Adjust the path to your users JSON file as needed
    with open("Backend/db/user_data.json", "r") as f:
        data = json.load(f)
        users = data.get("customer_users", [])
    for user in users:
        if user["username"] == username and user["password"] == password:
            print(f"Login successful. Welcome, {username}!")
            return Customer(**user)  # or return a Customer object if you want

    print("Login failed. Invalid username or password.")
    return None


if __name__ == "__main__":
    
    main()