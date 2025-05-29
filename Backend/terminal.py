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
            if user is not None:
                menu(user)
        else:
            print(f"Unknown command: {command}")

def menu(user):
    print(f"------main menu------")
    print("1 - View Catalogue")
    print("2 - View Cart")
    print("3 - Checkout")
    print("4 - Exit")


    choice = input("Enter your choice: ").strip()
    if choice == "1":
        view_catalogue(user)
    elif choice == "2":
        view_cart(user)
    elif choice == "3":
        check_out(user)
    elif choice == "4":
        print("Exiting Menu")
    else:
        print(f"Unknown option: {choice}") 

def view_catalogue(user: Customer):
    print(f"------Catalogue------")
    catalogue = Catalogue.get_instance()
    items = catalogue.get_all_items()
    if not items:
        print("No items available in the catalogue.")
        return
    print("\nCatalogue Items:")
    for item in items:
        print(f"{item.item_id}: {item.name} - ${item.price:.2f}")
    item_id = input("Enter item ID to add to cart (or 'q' to quit): ").strip()
    if item_id.lower() == 'q':
        return menu(user)
    else:
        try:
            item_id = int(item_id)
            item = catalogue.get_item_by_id(item_id)
            if item:
                user.cart.add_item(item)
                print(f"Added {item.name} to your cart.")
                menu(user)
            else:
                print(f"Item with ID {item_id} not found in the catalogue.")
                menu(user)
        except ValueError:
            print("Invalid item ID. Please enter a valid number.")
            menu(user)

def view_cart(user: Customer):
    cart = user.cart
    if not cart.items:
        print("Your cart is empty.")
        return menu(user)
    print("\nItems in your cart:")
    for item in cart.items:
        print(f"{item.item_id}: {item.name} - ${item.price:.2f}")
        
    menu_choice = input("Enter 'r' to remove an item or 'c' to checkout (or 'q' to quit): ").strip().lower()
    if menu_choice == 'r':
        item_id = input("Enter item ID to remove: ").strip()
        try:
            item_id = int(item_id)
            cart.remove_item(item_id)
            print(f"Removed item with ID {item_id} from your cart.")
            menu(user)
        except ValueError:
            print("Invalid item ID. Please enter a valid number.")
    elif menu_choice == 'c':
        check_out(user)
    else:
        print("Returning to main menu.")
        menu(user)


################does not work yet#####################
def check_out(user: Customer):
    cart = user.cart
    cart_items = cart.get_items()
    if not cart_items:
        print("Your cart is empty. Please add items to your cart before checking out.")
        return menu(user)
    print("\nCheckout:")
    print("Items in your cart:")
    for item in cart_items:
        print(f"- {item.name}: ${item.price:.2f}")
    total = cart.get_total()
    print(f"Sub Total: ${total:.2f}")

    shipping_details = cart.get_shipping_details()
    order = cart.checkout(shipping_details)
    user.orders.append(order)  

    print("\nOrder Summary:")
    print(f"Customer ID: {order.customer_id}")
    for item in order.items:
        print(f"- {item.name}: ${item.price:.2f}")
    print(f"Total: ${order.total:.2f}") 

#########################################################################

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