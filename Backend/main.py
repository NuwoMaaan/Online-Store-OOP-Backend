from models.user import User, Customer, Staff
from models.catalogue import Catalogue
from models.cart import Cart
from services.transaction_facade import TransactionFacade
from services.cart_service import CartService
from services.payment_service import PaymentService
from services.sales_service import SalesService
from services.order_service import OrderService
from services.user_service import UserService


transaction = TransactionFacade(OrderService(), PaymentService(), SalesService(), CartService())

def banner():
    print(r"""
      __          ________    ____        _ _               _____ _                 
     /\ \        / /  ____|  / __ \      | (_)             / ____| |                
    /  \ \  /\  / /| |__    | |  | |_ __ | |_ _ __   ___  | (___ | |_ ___  _ __ ___ 
   / /\ \ \/  \/ / |  __|   | |  | | '_ \| | | '_ \ / _ \  \___ \| __/ _ \| '__/ _ \
  / ____ \  /\  /  | |____  | |__| | | | | | | | | |  __/  ____) | || (_) | | |  __/
 /_/    \_\/  \/   |______|  \____/|_| |_|_|_|_| |_|\___| |_____/ \__\___/|_|  \___
""")
   

def main():
    banner()
    print("This is the terminal interface for the backend system.")
    print("You can run various commands to interact with the system.")
    
    while True:
        print("\nAvailable commands:")
        print("1 - Login")
        print("2 - Create account")
        print("3 - Exit")
        command = input("Enter command number: ").strip()
        if command == "3":
            print("Exiting terminal. Goodbye!")
            break
        elif command == "1":  
           user = UserService.login()
           if isinstance(user, Customer):
                menu(user)
           elif isinstance(user, Staff):
                staff_menu(user)

        elif command == "2":
            new_user = User.create_new_user()
            if new_user is None:
                print("Failed account creation")     
        else:
            print(f"Unknown command: {command}")

def menu(user):
    transaction = TransactionFacade(OrderService(), PaymentService(), SalesService(), CartService())
    while True:
        print(f"\n======main menu======")
        print("1 - View Catalogue")
        print("2 - View Cart")
        print("3 - Checkout")
        print("4 - Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            Catalogue.catalogue_menu(user)
            menu(user)
        elif choice == "2":
            Cart.cart_menu(user)
            menu(user)
        elif choice == "3":
            transaction.process(user)
        elif choice == "4":
            print("Exiting Menu")
            break
        else:
            print(f"Unknown option: {choice}") 

def staff_menu(user):
    while True:
        print(f"\n======Staff menu======")
        print("1 - Manage Catalogue")
        print("2 - Generate report")
        print("3 - Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            Catalogue.catalogue_staff()
            staff_menu(user)
        elif choice == "2":
            #generate_report() - Not implemented
            pass
        elif choice == "3":
            print("Exiting")
            break
        else:
            print(f"Unknown option: {choice}") 

    
    

if __name__ == "__main__":

    main()