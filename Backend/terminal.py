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
        catalogue = Catalogue.get_instance()
        while True:
            catalogue.view_catalogue()
            item_id = input("Enter item ID to add to cart (or 'q' to quit): ").strip()
            if item_id.lower() == 'q':
                break
            try:
                item_id = int(item_id)
                item = catalogue.get_item_by_id(item_id)
                if item:
                    user.cart.add_item(item)
                    print(f"Added {item.name} to your cart.")
                else:
                    print(f"Item with ID {item_id} not found in the catalogue.")
            except ValueError:
                print("Invalid item ID. Please enter a valid number or 'q' to quit.")
        menu(user)

    elif choice == "2":
        
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
                order = user.cart.checkout()
                order.order_summary()
                user.orders.append(order)
                break
            elif menu_choice == 'q':
                break
            else:
                print("Invalid option. Try again.")
        menu(user)

    elif choice == "3":
        order = user.cart.checkout()
        order.order_summary()
        user.orders.append(order)
    
    elif choice == "4":
        print("Exiting Menu")
    else:
        print(f"Unknown option: {choice}") 


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